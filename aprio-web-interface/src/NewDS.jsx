import { useState, useRef, useEffect } from "react";
import UploadLogo from "./images/UploadLogo";
import axios from "axios";
import { api } from "./env";


// TODO: Loading page while server is generating new set of rules
const clientId = Math.floor(Math.random() * 100000) + 1;
const NewDS = () => {

    const [stage, setStage] = useState("upload")
    const [file, setFile] = useState(null)
    const fileInputRef = useRef(null);
    const [error, setError] = useState(null)
    const [status, setStatus] = useState('')

    const handleFileChange = (event) => {
        // Update the state with the selected file
        setFile(event.target.files[0]);
      };
    
      const handleImageClick = () => {
        // Trigger the file input click when the image is clicked
        fileInputRef.current.click();
      };
      const accepted_formats = ['csv', 'xlsx']
      useEffect(()=>{
        if (file){

            

            if(accepted_formats.includes(file.name.split('.')[1])){
                setStage('submit')
            }else{
                setError("please upload a csv or an xlsx file")
                setTimeout(()=> {
                    setError(null)
                }, 3000)
            }
        }
      }, [file])
 

      useEffect(() => {
        if (stage === "processing") {

            upload_file_to_server()
        //   const CHUNK_SIZE = 1024*8; // Adjust the chunk size as needed
        //   const reader = new FileReader();

        }
    }, [stage, file]);

    const open_sock = async () => {

        console.log("connecting to websocket");
        const ws = new WebSocket(`ws://localhost:8000/train_websocket`);

        ws.onopen = () => {
            console.log("WebSocket is open now.");
            console.log('sending start signal to socket in 2 seconds');
            setTimeout(() => {
                ws.send('start')
            }, 2000);
        };

        ws.onmessage = (event) => {
            // Handle acknowledgment from the server
            console.log('Status:', event.data);
            setStatus(event.data)
        };

        ws.onclose = (event) => {
            console.log('WebSocket closed:', event.code, event.reason);
        };
    }

    const upload_file_to_server = async ()  => {
        const formData = new FormData();
  formData.append('file', file);
  try {

    const response = await axios.post(api+'NewDS', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    console.log('File uploaded successfully:', response.data);
    if(response.data.valid){
        console.log("okay, open socket now")
        open_sock()
    }else{
        setError("Features mismatch, please make sure the dataset is following the needed structure")
        setTimeout(()=>{
            setError(null)
            setFile(null)
            setStage('upload')
        }, 3000)
    }
  } catch (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Server responded with an error:', error.response.data);
      console.error('Status code:', error.response.status);
      console.error('Headers:', error.response.headers);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received from the server');
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error during request setup:', error.message);
    }

    console.error('Axios error config:', error.config);
  }

      }

    return ( 
        <div className="newDsPage" >

            {error && 
                <div className="error-container">
                    {error}
                </div>
            }

            {!error && stage == "upload" && 
                <div onClick={handleImageClick} className="upload-container" >

                    <UploadLogo />
                    <input
                        type="file"
                        ref={fileInputRef}
                        style={{ display: 'none' }}
                        onChange={handleFileChange}
                    />
                    <h2>Upload File</h2>
                </div>
            }
            {
                !error && stage === "submit"  &&
                <div className="submit-container">
                    <div className="info">
                        <div className="note">
                            <h4>IMPORTANT! make sure the dataset file contains the following features:</h4>
                            <ul className="features_list">
                                <li>InvoiceNo</li>
                                <li>StockCode</li>
                                <li>Description</li>
                                <li>Quantity</li>
                                <li>InvoiceDate</li>
                                <li>UnitPrice</li>
                                <li>CustomerID</li>
                                <li>Country</li>
                            </ul>
                        </div>
                        <div> Filename: <b>{file.name}</b></div>
                        <div>File Size: <b>{(file.size / (1024)).toFixed(4)} mb</b></div>
                    </div>
                    <div className="submit">
                        <button className="submit-btn" onClick={
                          ()=>{
                            setStage("processing")
                          }} >
                            Submit File
                        </button>
                    </div>
                </div>
            }

            {
                !error && stage === 'processing' &&
                <div className="status">
                    {status}
                </div>
            }
        </div>
     );
}
 
export default NewDS;