// A2A v1.0 Hello World server in Go with API key Bearer token verification.
package main

import (
	"context"
	"crypto/subtle"
	"fmt"
	"iter"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/a2aproject/a2a-go/v2/a2a"
	"github.com/a2aproject/a2a-go/v2/a2asrv"
)

type securedGoExecutor struct{}

func (e *securedGoExecutor) Execute(_ context.Context, execCtx *a2asrv.ExecutorContext) iter.Seq2[a2a.Event, error] {
	return func(yield func(a2a.Event, error) bool) {
		if execCtx.StoredTask == nil {
			if !yield(a2a.NewSubmittedTask(execCtx, execCtx.Message), nil) {
				return
			}
		}
		if !yield(a2a.NewStatusUpdateEvent(execCtx, a2a.TaskStateWorking, nil), nil) {
			return
		}

		userText := extractText(execCtx.Message)
		reply := fmt.Sprintf("Hello from Secured Go A2A Agent! API key verified. You said: %q", userText)

		evt := a2a.NewArtifactEvent(execCtx, a2a.NewTextPart(reply))
		evt.LastChunk = true
		if !yield(evt, nil) {
			return
		}
		yield(a2a.NewStatusUpdateEvent(execCtx, a2a.TaskStateCompleted, nil), nil)
	}
}

func (e *securedGoExecutor) Cancel(_ context.Context, execCtx *a2asrv.ExecutorContext) iter.Seq2[a2a.Event, error] {
	return func(yield func(a2a.Event, error) bool) {
		yield(a2a.NewStatusUpdateEvent(execCtx, a2a.TaskStateCanceled, nil), nil)
	}
}

func extractText(msg *a2a.Message) string {
	if msg == nil {
		return "World"
	}
	var parts []string
	for _, p := range msg.Parts {
		if t := p.Text(); t != "" {
			parts = append(parts, t)
		}
	}
	if len(parts) == 0 {
		return "World"
	}
	return strings.Join(parts, " ")
}

func requireAPIKey(expectedKey string, next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		const prefix = "Bearer "
		auth := r.Header.Get("Authorization")
		token := ""
		if len(auth) > len(prefix) && strings.EqualFold(auth[:len(prefix)], prefix) {
			token = strings.TrimSpace(auth[len(prefix):])
		}
		if subtle.ConstantTimeCompare([]byte(token), []byte(expectedKey)) != 1 {
			w.Header().Set("WWW-Authenticate", "Bearer")
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusUnauthorized)
			_, _ = w.Write([]byte(`{"error":{"code":401,"status":"UNAUTHENTICATED","message":"Missing or invalid Bearer API key token."}}`))
			return
		}
		next.ServeHTTP(w, r)
	})
}

func envOr(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func main() {
	host := envOr("A2A_HOST", "127.0.0.1")
	port := envOr("A2A_PORT", "9004")
	addr := fmt.Sprintf("%s:%s", host, port)
	baseURL := envOr("A2A_BASE_URL", "http://"+addr)
	expectedKey := envOr("A2A_API_KEY", "a2a-demo-secret-key")

	card := &a2a.AgentCard{
		Name:               "Secured Go Hello World Agent",
		Description:        "Go A2A v1.0 agent protected by Bearer API key verification.",
		Version:            "1.0.0",
		Capabilities:       a2a.AgentCapabilities{Streaming: true},
		DefaultInputModes:  []string{"text/plain"},
		DefaultOutputModes: []string{"text/plain"},
		SupportedInterfaces: []*a2a.AgentInterface{
			a2a.NewAgentInterface(baseURL, a2a.TransportProtocolHTTPJSON),
		},
		SecuritySchemes: a2a.NamedSecuritySchemes{
			"bearer_api_key": a2a.HTTPAuthSecurityScheme{
				Scheme:       "Bearer",
				BearerFormat: "APIKey",
				Description:  "Pass the API key via `a2a send --auth 'Bearer <API_KEY>'`",
			},
		},
		Skills: []a2a.AgentSkill{
			{
				ID:          "hello-go-auth",
				Name:        "Authenticated Go Greeting",
				Description: "Replies with a greeting when a valid Bearer API key is supplied.",
				Tags:        []string{"hello", "go", "auth", "a2a"},
				Examples:    []string{"Hello with an API key!"},
			},
		},
	}

	handler := a2asrv.NewHandler(&securedGoExecutor{})
	mux := http.NewServeMux()
	mux.Handle(a2asrv.WellKnownAgentCardPath, a2asrv.NewStaticAgentCardHandler(card))
	mux.Handle("/", requireAPIKey(expectedKey, a2asrv.NewRESTHandler(handler)))

	log.Printf("Secured Go A2A server listening on %s", baseURL)
	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatal(err)
	}
}
