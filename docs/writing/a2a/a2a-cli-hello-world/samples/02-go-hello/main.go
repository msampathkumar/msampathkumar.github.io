// Minimal A2A v1.0 Hello World server in Go.
package main

import (
	"context"
	"fmt"
	"iter"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/a2aproject/a2a-go/v2/a2a"
	"github.com/a2aproject/a2a-go/v2/a2asrv"
)

type helloGoExecutor struct{}

func (e *helloGoExecutor) Execute(_ context.Context, execCtx *a2asrv.ExecutorContext) iter.Seq2[a2a.Event, error] {
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
		reply := fmt.Sprintf("Hello from Go A2A Agent! You said: %q", userText)

		evt := a2a.NewArtifactEvent(execCtx, a2a.NewTextPart(reply))
		evt.LastChunk = true
		if !yield(evt, nil) {
			return
		}
		yield(a2a.NewStatusUpdateEvent(execCtx, a2a.TaskStateCompleted, nil), nil)
	}
}

func (e *helloGoExecutor) Cancel(_ context.Context, execCtx *a2asrv.ExecutorContext) iter.Seq2[a2a.Event, error] {
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

func envOr(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func main() {
	host := envOr("A2A_HOST", "127.0.0.1")
	port := envOr("A2A_PORT", "9002")
	addr := fmt.Sprintf("%s:%s", host, port)
	baseURL := envOr("A2A_BASE_URL", "http://"+addr)

	card := &a2a.AgentCard{
		Name:               "Go Hello World Agent",
		Description:        "Minimal A2A v1.0 Hello World agent built with a2a-go/v2.",
		Version:            "1.0.0",
		Capabilities:       a2a.AgentCapabilities{Streaming: true},
		DefaultInputModes:  []string{"text/plain"},
		DefaultOutputModes: []string{"text/plain"},
		SupportedInterfaces: []*a2a.AgentInterface{
			a2a.NewAgentInterface(baseURL, a2a.TransportProtocolHTTPJSON),
		},
		Skills: []a2a.AgentSkill{
			{
				ID:          "hello-go",
				Name:        "Go Greeting",
				Description: "Echoes a greeting from the Go A2A server.",
				Tags:        []string{"hello", "go", "a2a"},
				Examples:    []string{"Hello from A2A CLI!"},
			},
		},
	}

	handler := a2asrv.NewHandler(&helloGoExecutor{})
	mux := http.NewServeMux()
	mux.Handle(a2asrv.WellKnownAgentCardPath, a2asrv.NewStaticAgentCardHandler(card))
	mux.Handle("/", a2asrv.NewRESTHandler(handler))

	log.Printf("Go Hello World A2A server listening on %s", baseURL)
	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatal(err)
	}
}
