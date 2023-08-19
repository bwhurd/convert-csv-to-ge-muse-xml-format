import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
import os

def csv_to_muse_xml(input_path, output_path):
    # Load CSV data
    df = pd.read_csv(input_path)

    # Create the root Waveform element
    waveform = Element("Waveform")

    # Add WaveformType as Rhythm (assuming all data is rhythm data)
    waveform_type = SubElement(waveform, "WaveformType")
    waveform_type.text = "Rhythm"

    # Add SampleBase with a default value (this can be adjusted later if needed)
    sample_base = SubElement(waveform, "SampleBase")
    sample_base.text = "500"  # Assuming 500 samples per second

    # Iterate over the ECG lead columns in the dataframe and add them to the XML
    for lead in df.columns[1:]:  # Skipping the time column
        lead_data = SubElement(waveform, "LeadData")

        # Add LeadID
        lead_id = SubElement(lead_data, "LeadID")
        lead_id.text = lead

        # Add WaveFormData (joining all data points with spaces)
        wave_form_data = SubElement(lead_data, "WaveFormData")
        wave_form_data.text = " ".join(df[lead].dropna().astype(str))

    # Convert to formatted XML string
    xml_string = xml.dom.minidom.parseString(tostring(waveform)).toprettyxml(indent="   ")

    # Check if output file exists and handle filename
    counter = 1
    original_output_path = output_path
    while os.path.exists(output_path):
        output_path = original_output_path.replace('.xml', f'_0{counter}.xml')
        counter += 1

    # Save the XML to a file
    with open(output_path, "w") as xml_file:
        xml_file.write(xml_string)

if __name__ == "__main__":
    # Get the user's home directory
    user_home = os.path.expanduser("~")
    
    # Set the path to the Downloads folder
    downloads_path = os.path.join(user_home, 'Downloads')

    # Set the input and output file paths
    input_file = os.path.join(downloads_path, 'digitized_ecg_data.csv')
    output_file = os.path.join(downloads_path, 'digitized_ecg_data_muse.xml')
    
    csv_to_muse_xml(input_file, output_file)
