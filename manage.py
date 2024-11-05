# Import necessary modules
from django.utils.encoding import uri_to_iri

# Main function to demonstrate URI to IRI conversion
def main():
    # A URI containing non-ASCII characters
    uri = "https://example.com/path/%C3%A9cole"
    
    # Convert the URI to an IRI
    iri = uri_to_iri(uri)
    
    # Print the converted IRI
    print("Converted IRI:", iri)  # Expected output: https://example.com/path/école

# Run the main function
if __name__ == "__main__":
    main()