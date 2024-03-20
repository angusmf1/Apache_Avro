import io
import json
from avro.schema import parse
from avro.io import DatumReader, BinaryDecoder

# Reuse the load_schema function from your serializer to load the schemas
def load_schema(schema_file):
    with open(schema_file, 'r') as file:
        schema_json = json.load(file)
        schema = parse(json.dumps(schema_json))
        return schema

# Load each schema
recommendation_request_schema = load_schema('recommendation_request_schema.avsc')
movie_watch_schema = load_schema('movie_watch_schema.avsc')
movie_rating_schema = load_schema('movie_rating_schema.avsc')

# Function to decode Avro binary data given a schema
def decode_avro(binary_data, schema):
    bytes_reader = io.BytesIO(binary_data)
    decoder = BinaryDecoder(bytes_reader)
    reader = DatumReader(schema)
    return reader.read(decoder)

# Function to read and deserialize data from an Avro file
def read_from_avro(file_path, schema):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        decoded_data = decode_avro(binary_data, schema)
        print(decoded_data)

# Example usage: read data from the Avro files
print("Recommendation Requests:")
read_from_avro('data/recommendation_requests.avro', recommendation_request_schema)

print("\nMovie Watches:")
read_from_avro('data/movie_watches.avro', movie_watch_schema)

print("\nMovie Ratings:")
read_from_avro('data/movie_ratings.avro', movie_rating_schema)
