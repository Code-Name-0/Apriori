import logo from './logo.svg';
import './App.css';
import axios from "axios";

import {useState} from 'react'

const api = "http://127.0.0.1:8000/"

function App() {

  const [name, setName] = useState('')
  const [api_result, setApiResult] = useState(null)

  const post = () => {
    const body = {
      "name" : name
    }

    axios.post(api + "dummy_post", body).then(response => {
      setApiResult(response.data)
    })
  }

  const go_back = () => {
     setName('')
     setApiResult(null)
  }
 
  console.log(api_result)

  return (
    <div className="App">
      <header className="App-header">
        {!api_result ?
        <>
          <input placeholder='Enter you name' onChange={(e)=>setName(e.target.value)} value={name} />
          <button onClick={post} > Send </button>
        </>:
        <h1>
          <div>{api_result}</div>
          <button onClick={go_back} > Try another name... </button>
        </h1>}
      </header>
    </div>
  );
}

export default App;
