# Import modules
import streamlit as st
from pymongo.mongo_client import MongoClient
import dns
import certifi

# Page Layout
st.set_page_config(layout="wide")

# Title
st.title("LMS Software Repository Tool")

# Instructions
st.markdown("The LMS Software Repository Tool is used to capture and catalog all sofware developed by LMS at NASA GRC. Please enter the information into the fields below for each tool developed. Additionally, supply a zip file containing source code in the file selector, as well has any additional files (User Manul's, Reference Manuals, Input/Output Decks, etc.) where asked. Non-senstivie data is directly written to a MongoDB database, whereas sensative data will be saved locally as a text file that must be uploaded to the provided box link. All source code and supplementary files are saved to the LMS Github (https://github.com/bhearley/LMS-Software) and all additional information will be stored in Granta MI with links to the GitHub for each tool (https://granta.ndc.nasa.gov/mi/). Please contact Brandon Hearley (brandon.l.hearley@nasa.gov) for any questions/issues regarding the data collection tool or access to the GitHub and Granta MI. \n \n")

st.markdown('''---''')

# Tool Information
st.subheader('Tool Information')
tool_name = st.text_input("Software Tool Name:",value='', key = 'tool_name')
version = st.text_input("Version:",value='', key = 'version')
poc = st.text_input("Point of Contact:",value='', key = 'poc')
tool_desc = st.text_area("Tool Desciption:",value='', key = 'tool_desc')
keywords = st.text_area("Keywords:",value='', key = 'keywords', help = 'Enter keywords as comma separated list')
files = st.file_uploader('Upload Code', accept_multiple_files=True, type = ['zip'], key='file', help='Upload Compressed Folder For Storage in GitHub')
lang_opts = ['Python', 
             'MATLAB',
             'FORTRAN', 
             'C++', 
             'C#', 
             'R',
             'Java',
             'SQL',
             'HTML',
             'Other']
tool_lang = st.multiselect('Programming Language:', lang_opts, key='tool_lang')
tool_lang_other = st.text_input("Programming Languag (Other):",value='', key = 'tool_lang_other')

# Tool Applicaiton
st.subheader('Tool Application')
# -- Classification
class_opts = ['Analysis/Design', 
              'Deformation',
              'Damage','Lifing', 
              'Optimization', 
              'Thermal/Heat Transfer', 
              'Thermodynamics',
              'CFD',
              'Data Analysis',
              'Data Importing/Exporting',
              'Other']
tool_class = st.multiselect('Classificaton:', class_opts, key='tool_class')
tool_class_other = st.text_input("Classification (Other):",value='', key = 'tool_class_other')

# -- Material Application
mat_opts = ['Material Independent',
              'Metallic',
              'Ceramic',
              'Polymer',
              'Composite/Continuous',
              'Composite/Discontinuous',
              'Composite/Woven',
              'Multifunctional',
              'Smart',
              'Nano',
              'Fluid',
               'Other']
tool_mat = st.multiselect('Material Applicability:', mat_opts, key='tool_mat')
tool_mat_other = st.text_input("Material Applicability (Other):",value='', key = 'tool_mat_other')

# -- Material Description
direc_opts = ['Isotropic',
              'Anisotropic',
              'Transversley Isotropic',
              'Orthotropic']
mat_direc = st.multiselect('Material Directionality:', direc_opts, key='mat_direc')

scope_opts = ['Linear',
              'Nonlinear']
mat_scope = st.multiselect('Material Scope:', scope_opts, key='mat_scope')

def_opts = ['Linear Elastic',
            'Nonlinear Elastic',
            'Plastic',
            'Viscoelastic',
            'Viscoplastic']
mat_def = st.multiselect('Material Deformation:', def_opts, key='mat_def')


response_opts = ['Time Dependent',
                 'Time Independent']
mat_response = st.multiselect('Material Response:', response_opts, key='mat_response')

# -- Domain
length_opts = ['Atomistic',
               'Dislocation',
               'Nano',
               'Micro',
               'Consitituent',
               'Meso',
               'Laminate'
               'Macro',
               'Mutliscale'
               ]
mat_length = st.multiselect('Length Scale:', length_opts, key='mat_length')

time_opts = ['General',
             'Steady State',
             'Transient/Dynamic',
             'Quais-static'
               ]
mat_time = st.multiselect('Time Scale:', time_opts, key='mat_time')

ax_opts = ['1D',
           '2D',
           '3D',
             ]
mat_ax = st.multiselect('Multiaxiality:', ax_opts, key='mat_ax')

# Security/Availability
st.subheader('Security/Availability')
sec_opts = ['Unclassified',
            'Sensative But Unclassified (SBU)',
            'Classified',
             ]
sec_class = st.multiselect('Security Classification:', sec_opts, key='sec_class', max_selections=1)

avail_opts = ['Publicly Available',
              'Restricted',
              'Export Controlled',
              'Proprietary'
             ]
sec_avail = st.multiselect('Availability:', avail_opts, key='sec_avail', max_selections=1)

sens_opts = ['None',
             'ITAR',
             'EAR',
             'Limited Rights',
             'SBIR/STTR',
             'Trade Secret/Commercial Confidential',
             'Restrictred Rights Software'
             ]
sec_sens = st.multiselect('Sensitivity:', sens_opts, key='sec_sens')

dist_opts = ['Unlimited',
             'Authorized Personnel Only',
             'NASA Personnel Only',
             'U.S. Government Only',
             'U.S. Citizen Only',
             'U.S. Govt. & Govt. Contractors Only',
             'NASA Personnel & NASA Contractors Only',
             'NASA Contractors & U.S. Govt. Only'
             ]
sec_dist = st.multiselect('Distribution:', dist_opts, key='sec_dist', max_selections=1)

os_opts = ['Windows',
           'OSX',
           'Linux',
             ]
req_os = st.multiselect('Supported Operating Systems:', os_opts, key='req_os')

add_soft_num = st.number_input('Number of Additional Software Required:', min_value=0, max_value=None,key='add_soft_num')
grid_soft = st.columns(1)
add_soft = [] #Store additional software

    
# Add row to funding table
def add_row_soft(row):
    # -- Funding Source
    with grid_soft[0]:
        while len(add_soft) < row+1:
            add_soft.append(None)
        if row == 0:
            add_soft[row]=st.text_input('Additional Software Required', value='',key=f'input_coll{row}')
        else:
            add_soft[row]=st.text_input('Temp', value='',key=f'input_coll{row}',label_visibility = "collapsed")
    
# Add rows for number of funding sources
for r in range(int(add_soft_num)):
    add_row_soft(r)

# Manuals/References
st.subheader('Manuals/References')
user_man = st.file_uploader('Upload User Manual(s)', accept_multiple_files=True, key='user_man')
ref_man = st.file_uploader('Upload Reference Manual(s)', accept_multiple_files=True, key='ref_man')
other_files = st.file_uploader('Upload Other Documents', accept_multiple_files=True, key='other_files', help = "Other documents include example input/output decks, associated papers, reports, etc.")

sec_flag = 0
# Security Check
# -- If data is  Publicly Available and Not Sensitive, upload via MongoDB
sec_flag = 0  # Security Control Flag 
if sec_avail == [] or 'Publicly Available' in sec_avail:
  if sec_sens == [] or 'None' in sec_sens:
    sec_flag = 1
if st.button('Save to Database'):
    # Error Checking
    err_flag = 0
    # -- Required Attributes
    if tool_name == '':
      st.error('Software Tool Name must be populated.')
      err_flag = 1

    if poc == '':
      st.error('Point of Contact must be populated.')
      err_flag = 1
  
    if tool_desc == '':
      st.error('Tool Description must be populated.')
      err_flag = 1

    if tool_lang == [] and tool_lang_other == '':
      st.error('Programming Language must be populated.')
      err_flag = 1

    if err_flag == 0:
      # Create the new record
      new_rec = {}
      new_rec['Name'] = tool_name
      new_rec['Version'] = version
      new_rec['Point of Contact'] = poc
      new_rec['Description'] = tool_desc
      new_rec['Keywords'] = keywords
      new_rec['Langauge'] = tool_lang
      new_rec['Classification'] = tool_class
      new_rec['Classification Other'] = tool_class_other
      new_rec['Material Applicability'] = tool_mat
      new_rec['Material Applicability Other'] = tool_mat_other
      new_rec['Material Directionality'] = mat_direc
      new_rec['Material Scope'] = mat_scope
      new_rec['Material Deformation'] = mat_def
      new_rec['Material Response'] = mat_response
      new_rec['Length Scale'] = mat_length
      new_rec['Time Scale'] = mat_time
      new_rec['Multiaxiality'] = mat_ax
      new_rec['Material Directionality'] = mat_direc
      new_rec['Security Classification'] = sec_class
      new_rec['Availability'] = sec_avail
      new_rec['Sensitivity'] = sec_sens
      new_rec['Distribution'] = sec_dist
      new_rec['Time Scale'] = mat_time
      new_rec['OS'] = req_os
      if add_soft_num > 0:
        new_rec['Required Software'] = add_soft
      
      # ADD FILES
      new_rec['Source'] =[]
      for j in range(len(files)):
        new_rec['Source'].append(files[j].getvalue())
  
      new_rec['User Manuals'] =[]
      for j in range(len(user_man)):
        new_rec['User Manuals'].append([user_man[j].getvalue(), user_man[j].name])
  
      new_rec['Reference Manuals'] =[]
      for j in range(len(ref_man)):
        new_rec['Reference Manuals'].append([ref_man[j].getvalue(),ref_man[j].name])
  
      new_rec['Other Files'] =[]
      for j in range(len(other_files)):
        new_rec['Other Files'].append([other_files[j].getvalue(),other_files[j].name])
    
      # Write to MongoDB
      if sec_flag == 1:
        # Connect to Database 
        @st.cache_resource
        def init_connection():
            uri = "mongodb+srv://nasagrc:" + st.secrets['mongo1']['password'] + "@nasagrclabdatatest.hnx1ick.mongodb.net/?retryWrites=true&w=majority&appName=NASAGRCLabDataTest"
            return MongoClient(uri, tlsCAFile=certifi.where())
        
        # Create the Database Client
        client = init_connection()
        
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            st.write(e)
            print(e)
       
        # Load the Database and save the record
        db = client['LMS']
        collection = db['Software']
    
        # Delete Record if it already exists
        myquery = { "Name": tool_name}
        collection.delete_one(myquery)
    
        # Save New Record
        new_entry = collection.insert_one(new_rec)
        st.write('Saved to Database!')
  
      else:
        # Write Data to text file and have user upload to box
        data_out = ''
        keys = list(new_rec.keys())
        for i in range(len(keys)):
            data_out = data_out + str(keys[i]) + ': ' + str(new_rec[keys[i]]) + '\n'
        st.download_button('Download Sensative Data File', data_out, file_name = tool_name + '.txt')
      
if sec_flag == 0:
  st.write('Download the text file and upload to: https://nasagov.app.box.com/f/d6c56ef2755b49f8a64429662e3196f4')
