# Ensuring Data Quality in Machine Learning with Apache Avro
  
#### by Angus Ferrell, Graduate Student at Carnegie Mellon University                        
#### Mar 19, 2024

In the rapidly evolving world of machine learning (ML), the quality of data not only determines the accuracy of predictions but also the reliability and scalability of ML systems. As more organizations pivot towards data-driven decision-making, ensuring high-quality data becomes paramount. This is where Apache Avro, a data serialization system, comes into play. Let's delve into how Avro addresses data quality issues, particularly within the context of a movie streaming platform, and discuss its strengths and limitations for a general audience interested in machine learning.

## The Problem at Hand

Data quality issues can manifest in numerous ways: inconsistent data formats, missing values, or even the sheer incompatibility of data schema over time as systems evolve. In the realm of a movie streaming service, imagine the complexities involved in handling data from millions of users across the globe. The data encompasses not just user profiles but also their interactions, preferences, and viewing habits. Ensuring this vast ocean of data remains consistent, accessible, and scalable is a Herculean task, vital for personalized recommendations, billing, and content distribution.

## How Apache Avro Helps

Apache Avro steps in as a hero to tackle these challenges head-on. It's a data serialization framework that enables data schema and files to be processed by programs written in different languages. This is crucial for a movie streaming service that likely leverages various technologies across its data pipelines.

# Embracing Change: Schema Evolution in Data-Driven Applications with Apache Avro

In the dynamic world of data-driven applications, the structure of data can change as new features are added and existing features are refined. This evolution can create significant challenges in data management, particularly in terms of maintaining compatibility across different versions of data schemas. Apache Avro, a data serialization framework, offers a compelling solution to this problem through its support for schema evolution. Let's explore how Avro enables seamless schema changes, using a movie streaming service as our context.

## The Foundation: Data Schema with Apache Avro

Imagine a movie streaming service that logs various types of events: recommendation requests from users, movie watch activities, and user ratings for movies. To handle this data efficiently across different systems and languages, the service uses Apache Avro for data serialization. Avro requires schemas, defined in JSON, which describe the data structures for these events.

### Initial Data Schemas

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

## Navigating Change: Schema Evolution

As the streaming service evolves, it decides to collect additional information for each event type. This necessitates changes to the existing schemas—a process that could potentially disrupt the service's operations. However, with Avro's schema evolution capabilities, these changes can be made seamlessly.

### Evolving the Schemas

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

## The Impact of Schema Evolution

Schema evolution with Apache Avro allows the streaming service to adapt to changing requirements without the risk of data incompatibility. It ensures that data remains accessible and usable across different versions of the application, facilitating a smooth evolution of data infrastructure.

- **Backward Compatibility:** New systems can read data produced by old systems.
- **Forward Compatibility:** Old systems can ignore new fields added by newer systems.


Enhancing the "Parsing and Serialization Workflow" section of our blog post, we will dive deeper into how Avro facilitates efficient data handling and explore the pros and cons of using Avro for data serialization and deserialization within a streaming application context.

## Parsing and Serialization Workflow Enhanced

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

## Pros and Cons of Using Avro for Data Handling

### Pros

1. **Compact and Efficient**: Avro's binary format is more compact than other formats like JSON, reducing storage space and bandwidth usage.
2. **Schema Evolution**: Avro supports schema evolution, allowing for the addition of new fields to data structures without breaking existing data, facilitating backward and forward compatibility.
3. **Cross-Language Support**: Avro provides support for multiple languages, enabling data exchange between systems written in different languages.
4. **Strong Typing**: Avro enforces data types through its schema, improving data quality and error handling.

### Cons

1. **Schema Management**: Managing Avro schemas and ensuring they are accessible to all data consumers can introduce complexity, especially in large-scale systems.
2. **Initial Learning Curve**: Understanding Avro's serialization mechanisms and schema evolution features may require some initial learning effort.
3. **Tooling and Ecosystem**: While Avro is well-supported in the Hadoop ecosystem, its tooling and support in other contexts may not be as mature as other serialization formats.

In conclusion, Apache Avro offers a powerful solution for managing data serialization and deserialization in streaming applications. Its advantages in efficiency, schema evolution, and cross-language support make it an excellent choice for applications requiring compact data representation and robust data compatibility. However, the need for careful schema management and the initial learning curve are important considerations for teams adopting Avro.



## Conclusion



Apache Avro's schema evolution capabilities are essential for maintaining data compatibility and flexibility in evolving data-driven applications. By allowing schemas to evolve without breaking existing systems, Avro helps organizations like our hypothetical movie streaming service to innovate and adapt while ensuring data integrity and accessibility. As data schemas evolve to capture more nuanced information, Avro ensures that these changes enrich the application's ecosystem rather than disrupt it.


## Strengths and Limitations

### Strengths

- **Compatibility Management:** Avro's schema evolution mechanism is a significant strength. It helps manage data compatibility across different versions, reducing the risks of data corruption or loss.
- **Cross-Language Support:** Avro supports multiple languages, enabling seamless data interchange across diverse tech stacks within an organization.
- **Efficiency:** Avro's binary data format is both compact and fast, which is crucial for processing and storing vast amounts of data efficiently.

### Limitations

- **Learning Curve:** For teams not familiar with schema-based data serialization, there can be a learning curve to effectively implement and manage Avro schemas.
- **Tooling and Ecosystem:** While robust, Avro's tooling and ecosystem may not be as extensive or mature as some other serialization frameworks, potentially limiting integration options in certain tech stacks.

## Conclusion

Apache Avro offers a compelling solution to the challenges of data quality in machine learning applications. By facilitating schema evolution and ensuring data compatibility, it empowers teams to maintain and scale their ML systems effectively. Although it comes with its set of challenges, the benefits it brings to data consistency and efficiency make it a worthy consideration for any data-intensive application, such as a movie streaming service. As the landscape of machine learning continues to evolve, tools like Avro will be pivotal in ensuring that data, the lifeblood of ML, remains high-quality and reliable

.
