# Aesteroid Data Processor - Near-Earth Object Data Query and Analysis

Welcome to **Aesteroid Data Processor**, a robust Python project designed to filter, analyze, and save data related to Near-Earth Objects (NEOs) and their close approaches to Earth. This project showcases advanced programming techniques and highlights the skills acquired in object-oriented programming, abstract methods, and the design of extensible systems. The starter code and guideline is illustrated in project_instruction.md.

## Project Features

- **Extensible System Design**: The project is designed to support additional filters, output formats, and data sources with minimal code changes.
- **Object-Oriented Programming**: Core components of the system are implemented using OOP principles to ensure modularity and code reuse.
- **Abstract Methods and Subclassing**: Abstract base classes define shared interfaces, enabling flexible and extensible functionality.
- **Data Querying and Filtering**: Advanced filtering mechanisms allow users to query NEO data based on various criteria such as approach distance, velocity, and hazard potential.
- **Dynamic Data Limiting**: Results can be dynamically limited to a specific number of entries.
- **Data Serialization**: Supports serialization of complex objects for CSV and JSON output formats, ensuring interoperability with other tools and systems.

## Key Skills Demonstrated

### 1. Object-Oriented Programming (OOP)
- Utilized OOP principles like encapsulation, inheritance, and polymorphism to create modular and maintainable code.
- Designed the `AttributeFilter` class as a reusable superclass for various attribute-based filters.

### 2. Abstract Methods and Interfaces
- Defined abstract methods in `AttributeFilter` to enforce implementation of custom filtering logic in subclasses.
- Leveraged Python's `abc` module to ensure a clean and extensible design.

### 3. System Extensibility
- Built a filter system that allows easy addition of new filters by subclassing.
- Designed output functions (`write_to_csv`, `write_to_json`) to handle multiple data serialization formats.

### 4. Data Handling and Serialization
- Implemented robust serialization methods for both CSV and JSON formats.
- Addressed edge cases, such as missing values, through thoughtful design and default handling.

### 5. Functional Programming and Generators
- Employed Python generators for efficient, on-demand data processing, particularly in filtering and limiting results.

### 6. Real-World Problem Solving
- Worked with NEO datasets to solve practical problems related to data filtering, analysis, and reporting.

## How It Works

### Core Components

1. **AttributeFilter and Subclasses**
   - `AttributeFilter`: A superclass that defines the interface for filtering NEO data.
   - Subclasses (e.g., `DistanceFilter`, `VelocityFilter`) implement the `get` method to fetch specific attributes for filtering.

2. **Query System**
   - `query()`: Dynamically filters close approaches using multiple filter criteria.

3. **Result Limiting**
   - `limit()`: Dynamically limits the number of results from a generator.

4. **Output Handlers**
   - `write_to_csv`: Serializes results into a structured CSV file.
   - `write_to_json`: Serializes results into a well-formatted JSON file.

### Example Workflow

1. Query the dataset using user-defined filters.
2. Limit the number of results.
3. Save the output to either CSV or JSON format.

## Technologies Used

- **Programming Language**: Python
- **Data Handling**: `csv` and `json` modules
- **Object-Oriented Design**: Abstract classes and inheritance
- **Iterators and Generators**: Efficient data streaming

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/neo-analytics.git
   cd neo-analytics
   ```

2. Run the main script to query and filter data:
   ```bash
   python main.py
   ```

3. Specify output format and file path:
   ```bash
   python main.py --output-format csv --output-path results.csv
   ```

## Potential Use Cases

- Analyzing close approaches of celestial bodies to Earth for scientific research.
- Filtering hazardous NEOs for risk assessment.
- Building a foundation for advanced data processing pipelines.


