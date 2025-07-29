import os
import vertexai

from vertexai import rag

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

vertexai.init(project=PROJECT_ID, location=LOCATION)


class RagCorpusManager:
    def __init__(self, rag_dataset_folder="rag_dataset"):
        self.rag_dataset_folder = rag_dataset_folder
        self.rag_corpus_name_file = ".rag"
        self.rag_corpus = None

        rag_corpus_name = None
        if os.path.exists(self.rag_corpus_name_file):
            with open(self.rag_corpus_name_file, "r") as f:
                rag_corpus_name = f.read().strip()

        if rag_corpus_name:
            try:
                print(f"Loading existing RAG corpus: {rag_corpus_name}")
                self.rag_corpus = rag.get_corpus(name=rag_corpus_name)
            except Exception as e:
                print(
                    f"Failed to load corpus {rag_corpus_name}: {e}. Creating a new one."
                )
                self._create_rag_corpus()
        else:
            self._create_rag_corpus()

    def _create_rag_corpus(self):
        print("Creating new RAG corpus...")
        self.rag_corpus = rag.create_corpus(display_name="my-rag-corpus")
        with open(self.rag_corpus_name_file, "w") as f:
            f.write(self.rag_corpus.name)
        self._upload_files()

    def _upload_files(self):
        print(f"Uploading files from: {self.rag_dataset_folder}")
        if not os.path.exists(self.rag_dataset_folder):
            os.makedirs(self.rag_dataset_folder)
            print(f"Created directory: {self.rag_dataset_folder}")
            # You can add some default files here if you want
            with open(os.path.join(self.rag_dataset_folder, "sample.txt"), "w") as f:
                f.write("This is a sample file for the RAG corpus.")

        # Upload all files to the RAG corpus
        for filename in os.listdir(self.rag_dataset_folder):
            filepath = os.path.join(self.rag_dataset_folder, filename)
            if os.path.isfile(filepath):
                print(f"Uploading file: {filename}")
                rag.upload_file(
                    corpus_name=self.rag_corpus.name,
                    path=filepath,
                    display_name=filename,
                )

    def list_files(self):
        """Lists all files in the RAG corpus with their status."""
        print("Listing files in RAG corpus...")
        if not self.rag_corpus:
            print("Corpus not initialized.")
            return

        files = list(rag.list_files(self.rag_corpus.name))
        for i, each in enumerate(files, 1):
            print(
                f"{i} | file: {each.display_name} | status: {str(each.file_status).strip()} | full name: {each.name}"
            )
        print(f"Total number of files: {len(files)}")

    def delete_corpus(self):
        """Deletes the RAG corpus and the local tracking file."""
        if not self.rag_corpus:
            print("No RAG corpus to delete.")
            return

        print(f"Deleting RAG corpus: {self.rag_corpus.name}")
        try:
            rag.delete_corpus(name=self.rag_corpus.name)
            if os.path.exists(self.rag_corpus_name_file):
                os.remove(self.rag_corpus_name_file)
            self.rag_corpus = None
            print("RAG corpus deleted.")
        except Exception as e:
            print(f"Error deleting corpus: {e}")

    def _cleanup_files(self, local_filenames, corpus_files):
        """Deletes files from the corpus that are not in the local file list."""
        print("Cleaning up old files from RAG corpus...")
        corpus_filenames = {f.display_name for f in corpus_files}
        files_to_delete = corpus_filenames - local_filenames

        if not files_to_delete:
            print("No old files to delete.")
            return

        for rag_file in corpus_files:
            if rag_file.display_name in files_to_delete:
                print(f"Deleting old file: {rag_file.display_name}")
                rag.delete_file(name=rag_file.name)

    def refresh(self):
        """Synchronizes the RAG corpus with the local dataset folder."""
        print("Refreshing RAG corpus...")
        if not self.rag_corpus:
            print("Corpus not initialized.")
            return

        # Get local files as a set
        local_filenames = {
            f
            for f in os.listdir(self.rag_dataset_folder)
            if os.path.isfile(os.path.join(self.rag_dataset_folder, f))
        }

        # Get corpus files (one API call)
        corpus_files = list(rag.list_files(corpus_name=self.rag_corpus.name))
        corpus_filenames = {f.display_name for f in corpus_files}

        # Upload new files
        files_to_upload = local_filenames - corpus_filenames
        if not files_to_upload:
            print("No new files to upload.")
        else:
            print("Uploading new files...")
            for filename in files_to_upload:
                print(f"Uploading new file: {filename}")
                filepath = os.path.join(self.rag_dataset_folder, filename)
                rag.upload_file(
                    corpus_name=self.rag_corpus.name,
                    path=filepath,
                    display_name=filename,
                )

        # Delete old files
        self._cleanup_files(local_filenames, corpus_files)

    def rag_query(self, query_text):
        """Query the RAG corpus and return top_k results."""
        response = rag.retrieval_query(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=self.rag_corpus.name,
                )
            ],
            rag_retrieval_config=rag.RagRetrievalConfig(
                top_k=10,  # Optional
                filter=rag.Filter(
                    vector_distance_threshold=0.5,  # Optional
                ),
            ),
            text=query_text,
        )
        context = " ".join(
            [context.text for context in response.contexts.contexts]
        ).replace("\n", "")
        print(f"Query: {query_text}")
        print(f"Context: {context}")
        return context

    def main(self):
        self.refresh()
        return self.rag_corpus.name


if __name__ == "__main__":
    rag_manager = RagCorpusManager()
    print(f"RAG Corpus Name: {rag_manager.rag_corpus.name}")
    # list files
    rag_manager.list_files()
    # refresh files
    rag_manager.refresh()
    # rag_manager.delete_corpus()
    response = rag_manager.rag_query("What is project status?")
    print(response)
