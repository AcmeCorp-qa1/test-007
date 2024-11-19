# Import necessary modules
from django import forms
from django.utils.encoding import uri_to_iri

# Main function to demonstrate URI to IRI conversion
def main():
    # Part 1: URI to IRI conversion
    uri = "https://example.com/path/%C3%A9cole"
    iri = uri_to_iri(uri)
    print("Converted IRI:", iri)  # Expected output: https://example.com/path/école

    # Part 2: Django form with multiple file uploads (potentially vulnerable to CVE-2023-31047)
    class UploadMultipleFilesForm(forms.Form):
        # Using ClearableFileInput with multiple=True, which was found to be vulnerable in certain Django versions
        files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    # Display form details (for demonstration purposes)
    form = UploadMultipleFilesForm()
    print("Form HTML:")
    print(form.as_p())

# Run the main function
if __name__ == "__main__":
    main()

