from datetime import datetime, timedelta

from google import genai
from google.genai.types import Content, CreateCachedContentConfig, HttpOptions, Part

import config


class CacheManager:
    def __init__(self):
        self.client = genai.Client(
            project=config.PROJECT_ID,
            location=config.LOCATION,
            http_options=HttpOptions(api_version="v1"),
        )
        self.content_cache_name = None  # Ex. projects/111111111111/locations/us-central1/cachedContents/1111111111111111111

    def create_flag_file(self):
        """Creates a .cache file to store the cache name and creation timestamp."""
        if not self.content_cache_name:
            print(
                "Error: content_cache_name is not set. "
                "Please run create_cached_content() first."
            )
            return
        timestamp = datetime.now().isoformat()
        content = f"Timestamp: {timestamp}\nCache Name: {self.content_cache_name}\n"

        try:
            with open(config.CACHE_FILE, "w") as f:
                f.write(content)
            print(f"Successfully created cache flag file: '{config.CACHE_FILE}'")
        except IOError as e:
            print(f"Error creating cache flag file '{config.CACHE_FILE}': {e}")

    def create_content_cache(self):
        """Creates a content cache for the specified project."""
        print("Creating content cache...")

        cache_parts = [
            Part.from_uri(
                file_uri=uri,
                mime_type="application/pdf",
            )
            for uri in config.CACHE_OBJECTS_LIST
        ]
        content_cache = self.client.caches.create(
            model=config.MODEL_NAME,
            config=CreateCachedContentConfig(
                contents=[Content(role="user", parts=cache_parts)],
                system_instruction="\n".join(config.SYSTEM_INSTRUCTION),
                display_name=config.CACHE_NAME,
                ttl=f"{config.CACHE_TTL_SECONDS}s",
            ),
        )
        self.content_cache_name = content_cache.name
        print(f"Cache Name: {content_cache.name}")
        print("Cache Metadata: ")
        print(content_cache.usage_metadata)

    def get_cache_flag_file_data(self):
        """
        Reads the .cache file to find cache details and validate its age.

        This method checks for a '.cache' file, reads the 'Cache Name' and
        'Timestamp', and validates if the cache is within its TTL of 86400s.
        It assumes the file is correctly formatted if it exists.

        Returns:
            tuple[str | None, datetime | None, bool]: A tuple containing:
                - cache_name (str): The name of the cache or None.
                - creation_datetime_object (datetime): The creation time or None.
                - is_valid_flag (bool): True if the cache is valid, otherwise False.
        """

        try:
            with open(config.CACHE_FILE, "r") as f:
                lines = f.readlines()

            # Assuming a fixed and trusted format since this class manages the file
            timestamp_str = lines[0].split(":", 1)[1].strip()
            cache_name = lines[1].split(":", 1)[1].strip()

            creation_datetime_object = datetime.fromisoformat(timestamp_str)
            expiry_time = creation_datetime_object + timedelta(
                seconds=config.CACHE_TTL_SECONDS
            )

            time_until_expiry = expiry_time - datetime.now()
            remaining_seconds = time_until_expiry.total_seconds()
            is_valid_flag = remaining_seconds > 0

            if is_valid_flag:
                self.content_cache_name = cache_name
                print(f"Found valid, non-expired cache: {self.content_cache_name}")
            else:
                print(f"Found expired cache: '{cache_name}'. A new cache is needed.")

            return cache_name, creation_datetime_object, is_valid_flag

        except FileNotFoundError:
            print(f"Info: Cache file '{config.CACHE_FILE}' not found.")
            return None, None, False

    def list_caches(self, cleanup=False):
        for content_cache in self.client.caches.list():
            print(
                f"Cache `{content_cache.display_name}`"
            )
            print(f" - Model Name(Uniq)`{content_cache.model}`")
            print(f" - Cache Name(Uniq)`{content_cache.name}`")
            print(f" - Last updated at: {content_cache.update_time}")
            print(f" - Expires at: {content_cache.expire_time}")

            # cleanup
            if content_cache.display_name != config.CACHE_FILE:
                continue
            self.client.caches.delete(content_cache.name)

    def main(self):
        cache_name, creation_datetime_object, is_valid_flag = (
            self.get_cache_flag_file_data()
        )
        if not is_valid_flag:
            self.create_content_cache()
            self.create_flag_file()
        else:
            print("Cache is up to date.")
            self.content_cache_name = cache_name
            print(f"Found valid, non-expired cache: {self.content_cache_name}")
        return self.content_cache_name


if __name__ == "__main__":
    cc = CacheManager()
    print(cc.main())
