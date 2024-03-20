import csv
import io
import json
import re
from avro.schema import parse
from avro.io import DatumWriter, BinaryEncoder


# Function to load an Avro schema from a .avsc file
def load_schema(schema_file):
    with open(schema_file, 'r') as file:
        schema_json = json.load(file)
        # Correctly use the avro.schema.parse function
        schema = parse(json.dumps(schema_json))
        return schema

# Load each schema
recommendation_request_schema = load_schema('recommendation_request_schema.avsc')
movie_watch_schema = load_schema('movie_watch_schema.avsc')
movie_rating_schema = load_schema('movie_rating_schema.avsc')


def parse_movie_watch(entry):
    # The regex pattern is adjusted to match the given log entry format
    match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}),(\d+),GET /data/m/(.+?)/(\d+)\.mpg', entry)
    if not match:
        print(f"Unexpected format for Movie Watch log entry: {entry}")
        return None  # Returning None to indicate a parsing failure

    time, userid, movieid, minute = match.groups()
    return {
        "time": time,
        "userid": int(userid),
        "movieid": movieid.replace('+', ' '),
        "minute": minute
    }


def parse_recommendation(log_entry):
    recommendation_match = re.search(
        r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+),(\d+),recommendation request (.*?), status (.*?), result: (.*?), (\d+) ms', 
        log_entry
    )
    
    if recommendation_match:
        time, userid, server, status, results, responsetime = recommendation_match.groups()
        
        # Convert userid and status to int, split results into a list, and responsetime as is (string with ' ms')
        userid = int(userid)
        status = int(status)
        recommendations = results.split(', ')
        
        return {
            "time": time,
            "userid": userid,
            "server": server,
            "status": status,
            "recommendations": recommendations,
            "responsetime": responsetime + " ms"  # Append ' ms' to match the original schema
        }
    
    else:
        print(f"Could not parse recommendation log entry: {log_entry}")
        return None


def parse_rating(log_entry):
    parts = log_entry.split(',')
    time = parts[0]
    userid = int(parts[1])
    movie_rating = parts[2].split('=')    
    movieid = movie_rating[0].split('/')[-1]
    rating = movie_rating[1]
    
    return {
        "time": time,
        "userid": userid,
        "movieid": movieid,
        "rating": rating
    }

# Function to encode a dictionary to Avro binary format given a schema
def encode_avro(data, schema):
    writer = DatumWriter(schema)
    bytes_writer = io.BytesIO()
    encoder = BinaryEncoder(bytes_writer)
    writer.write(data, encoder)
    return bytes_writer.getvalue()

# Function to identify and parse log entry types based on provided schemas
def identify_and_parse_log_entry(log_type, log_entry):
    if log_type == "Recommendation":
        data = parse_recommendation(log_entry)
        return data, recommendation_request_schema if data else (None, None)
    elif log_type == "Movie":
        data = parse_movie_watch(log_entry)
        return data, movie_watch_schema if data else (None, None)
    elif log_type == "Rating":
        data = parse_rating(log_entry)
        return data, movie_rating_schema if data else (None, None)
    else:
        print(f"Skipping unknown log entry type: {log_type}")
        return None, None

# Prepare file paths for each log type
file_paths = {
    "Recommendation": "data/recommendation_requests.avro",
    "Movie": "data/movie_watches.avro",
    "Rating": "data/movie_ratings.avro"
}

# Using context managers for file operations
with open('data/master.csv', mode='r') as csvfile, \
     open(file_paths["Recommendation"], "wb") as rec_file, \
     open(file_paths["Movie"], "wb") as movie_file, \
     open(file_paths["Rating"], "wb") as rating_file:

    file_objects = {
        "Recommendation": rec_file,
        "Movie": movie_file,
        "Rating": rating_file
    }
    
    reader = csv.DictReader(csvfile)
    for row in reader:
        parsed_data, schema = identify_and_parse_log_entry(row['Type'], row['Log Entry'])
        if parsed_data is not None and schema:
            binary_data = encode_avro(parsed_data, schema)
            file_objects[row['Type']].write(binary_data)
        else:
            print(f"Skipping log entry due to parsing error: {row['Log Entry']}")

print("Binary Avro data has been written to files.")
