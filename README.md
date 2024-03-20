# Streamlining Data Handling in Machine Learning Applications with Apache Avro
  
#### by Angus Ferrell, Graduate Student at Carnegie Mellon University                        
#### Mar 19, 2024

In the fast-paced domain of machine learning (ML), data serves as the cornerstone upon which predictive models and algorithms stand. The quality of this data directly influences not only the accuracy of predictions but also the overall reliability and scalability of ML systems. Amidst this backdrop, Apache Avro emerges as a pivotal tool, designed to tackle the multifaceted challenges associated with data serialization and ensuring the high quality of data. This blog post aims to demystify how Apache Avro can be effectively leveraged, especially within the context of a movie streaming platform, providing insights into its operational strengths and limitations.

### Understanding the Challenge
Data quality issues, characterized by inconsistent formats, missing values, or schema incompatibilities due to evolving systems, pose significant hurdles. Consider the intricacies of managing data in a movie streaming service – from user profiles and preferences to their viewing habits and interactions. The Herculean task of maintaining data consistency, accessibility, and scalability across millions of global users is critical for personalized content recommendations, accurate billing, and efficient content distribution.

### How Apache Avro Offers a Solution
Apache Avro steps onto the scene as a formidable ally, offering a schema-based data serialization framework that allows for efficient data processing across different programming languages. This attribute is especially beneficial for a movie streaming service that utilizes a diverse technological stack across its data pipelines.

## Embracing Change: Schema Evolution in Data-Driven Applications with Apache Avro

In the dynamic world of data-driven applications, the structure of data can change as new features are added and existing features are refined. This evolution can create significant challenges in data management, particularly in terms of maintaining compatibility across different versions of data schemas. Apache Avro, a data serialization framework, offers a compelling solution to this problem through its support for schema evolution. Let's explore how Avro enables seamless schema changes, using a movie streaming service as our context.

### The Foundation: Data Schema with Apache Avro

Imagine a movie streaming service that logs various types of events: recommendation requests from users, movie watch activities, and user ratings for movies. To handle this data efficiently across different systems and languages, the service uses Apache Avro for data serialization. Avro requires schemas, defined in JSON, which describe the data structures for these events.

#### Initial Data Schemas

Initially, the streaming service defines the following Avro schemas for its events:

```python
from avro.schema import parse

# Schema for Recommendation Request Events
recommendation_request_schema_json = '''
{
  "type": "record",
  "name": "RecommendationRequest",
  "fields": [
    {"name": "time", "type": "string"},
    {"name": "userId", "type": "string"},
    {"name": "server", "type": "string"},
    {"name": "status", "type": "int"},
    {"name": "recommendations", "type": ["null", "string"], "default": null},
    {"name": "responseTime", "type": "int"}
  ]
}
'''

# Schema for Movie Watch Events
movie_watch_event_schema_json = '''
{
  "type": "record",
  "name": "MovieWatchEvent",
  "fields": [
    {"name": "time", "type": "string"},
    {"name": "userId", "type": "string"},
    {"name": "movieId", "type": "string"},
    {"name": "minute", "type": "int"}
  ]
}
'''

# Schema for Movie Rating Events
movie_rating_event_schema_json = '''
{
  "type": "record",
  "name": "MovieRatingEvent",
  "fields": [
    {"name": "time", "type": "string"},
    {"name": "userId", "type": "string"},
    {"name": "movieId", "type": "string"},
    {"name": "rating", "type": "int"}
  ]
}
'''

# Parse schemas
recommendation_request_schema = parse(recommendation_request_schema_json)
movie_watch_event_schema = parse(movie_watch_event_schema_json)
movie_rating_event_schema = parse(movie_rating_event_schema_json)
```

These schemas lay the groundwork for consistent data handling across the streaming service's ecosystem.

### Navigating Change: Schema Evolution

As the streaming service evolves, it decides to collect additional information for each event type. This necessitates changes to the existing schemas—a process that could potentially disrupt the service's operations. However, with Avro's schema evolution capabilities, these changes can be made seamlessly.

#### Evolving the Schemas

The service updates its schemas to include new fields: `deviceType` for recommendation requests, `watchedInFull` for movie watch events, and `ratingContext` for movie ratings.

```python
# Evolved Schema for Recommendation Request Events
recommendation_request_schema_evolved_json = '''
{
  "type": "record",
  "name": "RecommendationRequest",
  "fields": [
    {"name": "time", "type": "string"},
    {"name": "userId", "type": "string"},
    {"name": "server", "type": "string"},
    {"name": "status", "type": "int"},
    {"name": "recommendations", "type": ["null", "string"], "default": null},
    {"name": "responseTime", "type": "int"},
    {"name": "deviceType", "type": ["null", "string"], "default": null}  # New field
  ]
}
'''

# Parse evolved schemas
recommendation_request_schema_evolved = parse(recommendation_request_schema_evolved_json)
```

The new fields are added with default values, ensuring that new data can still be processed by systems using the old schemas, and old data can be understood by systems using the new schemas. This backward and forward compatibility is a cornerstone of Avro's design.

### The Impact of Schema Evolution

Schema evolution with Apache Avro allows the streaming service to adapt to changing requirements without the risk of data incompatibility. It ensures that data remains accessible and usable across different versions of the application, facilitating a smooth evolution of data infrastructure.

- **Backward Compatibility:** New systems can read data produced by old systems.
- **Forward Compatibility:** Old systems can ignore new fields added by newer systems.


Enhancing the "Parsing and Serialization Workflow" section of our blog post, we will dive deeper into how Avro facilitates efficient data handling and explore the pros and cons of using Avro for data serialization and deserialization within a streaming application context.

## Enhanced Parsing and Serialization Workflow

Apache Avro provides a robust framework for data serialization, enabling the conversion of complex data structures into a compact binary format. This serialization process is essential for efficient data storage and fast data transmission.

### Serialization in Action

Serialization involves translating data structures or object states into a format that can be stored or transmitted and then reconstructing the original object from the serialized data. Here's a practical example of serialization:

```python
def encode_avro(data, schema):
    writer = DatumWriter(schema)
    bytes_writer = io.BytesIO()
    encoder = BinaryEncoder(bytes_writer)
    writer.write(data, encoder)
    return bytes_writer.getvalue()
```

In our streaming application, log entries are processed as follows:

1. **Log Entry Loading**: Log entries are read from a CSV file, `data/master.csv`.
2. **Log Entry Parsing**: Each log entry is parsed according to its type—recommendation requests, movie watches, or movie ratings.
3. **Data Serialization**: Parsed data is serialized using the appropriate Avro schema.
4. **Data Writing**: Serialized data is written to Avro files, organized by log entry type.

### Deserialization in Action

Deserialization is crucial for reading and processing the serialized data. It involves converting the binary data back into its original form based on the schema used during serialization.

```python
def decode_avro(binary_data, schema):
    bytes_reader = io.BytesIO(binary_data)
    decoder = BinaryDecoder(bytes_reader)
    reader = DatumReader(schema)
    return reader.read(decoder)
```

### Practical Application

To process the serialized data:

1. **Reading Serialized Data**: Data is read from Avro files, such as `data/recommendation_requests.avro`.
2. **Data Deserialization**: The binary data is deserialized into its original structure for analysis or further processing.

```python
# Example: Reading and processing data from 'data/recommendation_requests.avro'
recommendation_data = read_from_avro('data/recommendation_requests.avro', recommendation_request_schema)
```

Apache Avro is a serialization framework that offers efficient data handling capabilities, especially for streaming and machine learning applications. It presents a balanced approach to data management, blending compact storage and efficient processing with robust support for schema evolution and cross-language interoperability. This makes Avro particularly suited for applications requiring not just compact data representation but also a high degree of data compatibility and flexibility.

### Advantages of Avro

- **Efficiency and Compactness**: Avro's binary data format significantly reduces storage space and bandwidth usage compared to text-based formats like JSON.
- **Schema Evolution**: Supports adding new fields to data structures without impacting existing data, ensuring both backward and forward compatibility. This is particularly beneficial for evolving data-driven applications, such as movie streaming services, where data schemas might need to adapt over time.
- **Cross-Language Support**: Facilitates data exchange between systems written in different programming languages, enhancing interoperability within diverse tech ecosystems.
- **Strong Typing**: By enforcing data types through schemas, Avro improves data quality and simplifies error handling, making it easier to maintain data integrity across complex systems.

### Challenges of Avro

- **Schema Management**: Ensuring that Avro schemas are consistently accessible and understood across all data consumers can introduce complexity, particularly in larger systems.
- **Learning Curve**: New users may find Avro's serialization mechanisms and schema evolution concepts initially challenging, requiring a period of learning and adjustment.
- **Tooling and Ecosystem**: While Avro is well-integrated within the Hadoop ecosystem, its tooling and broader ecosystem support might lag behind other serialization formats, potentially limiting its application in certain contexts.

### Final Thoughts

Apache Avro's strength lies in its schema evolution capabilities and its efficiency in handling large volumes of data. These features are essential for maintaining data quality and compatibility in dynamic, data-intensive environments. Avro is particularly valuable for applications like movie streaming services that continuously adapt and evolve, requiring flexible and reliable data management solutions. Despite the challenges related to schema management and the initial learning curve, the strategic advantages of using Avro—especially in terms of data compatibility and efficiency—make it a compelling choice for many applications. As machine learning and data-driven technologies continue to advance, tools like Avro will play a crucial role in ensuring that data remains a reliable and effective foundation for innovation and growth.
