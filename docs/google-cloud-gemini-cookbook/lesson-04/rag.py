import os
import vertexai

from vertexai import rag


PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

vertexai.init(project=PROJECT_ID, location=LOCATION)


class RagManager:
    def __init__(self, rag_dataset_folder="rag_dataset"):
        self.rag_dataset_folder = rag_dataset_folder
        self.rag_corpus_name_file = ".rag"
        self.rag_corpus = None

        if os.path.exists(self.rag_corpus_name_file):
            with open(self.rag_corpus_name_file, "r") as f:
                rag_corpus_name = f.read().strip()
            if rag_corpus_name:
                print(f"Loading existing RAG corpus: {rag_corpus_name}")
                self.rag_corpus = rag.get_corpus(name=rag_corpus_name)
            else:
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
        print("Listing files in RAG corpus...")
        i = 1
        for each in rag.list_files(self.rag_corpus.name):
            print(f'{i} |file: {each.display_name} | status: {str(each.file_status).strip()} | full name: {each.name}')
            i = i + 1
        print(f"Total number of files: {i}")

    def delete_corpus(self):
        print("Deleting RAG corpus...")
        rag.delete_corpus(name=self.rag_corpus.name)
        os.remove(self.rag_corpus_name_file)
        self.rag_corpus = None
        print("RAG corpus deleted.")



    def refresh(self):
        print("Refreshing RAG corpus...")
        # Get local files
        local_files = [f for f in os.listdir(self.rag_dataset_folder) if os.path.isfile(os.path.join(self.rag_dataset_folder, f))]

        # Get corpus files
        corpus_files = [f.display_name for f in rag.list_files(corpus_name=self.rag_corpus.name)]

        # Upload new files
        for filename in local_files:
            if filename not in corpus_files:
                print(f"Uploading new file: {filename}")
                filepath = os.path.join(self.rag_dataset_folder, filename)
                rag.upload_file(
                    corpus_name=self.rag_corpus.name,
                    path=filepath,
                    display_name=filename,
                )

        # Delete old files
        for rag_file in rag.list_files(corpus_name=self.rag_corpus.name):
            if rag_file.display_name not in local_files:
                print(f"Deleting old file: {rag_file.display_name}")
                rag.delete_file(name=rag_file.name)


# rag_manager = RagManager()
# print(f"RAG Corpus Name: {rag_manager.rag_corpus.name}")
# rag_manager.refresh()