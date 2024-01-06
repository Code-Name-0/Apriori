import logo from './logo.svg';
import './App.css';
import axios from "axios";
import Main from './Main';
import {useState} from 'react'
import { api } from './env';
import { Navbar } from './components';

function App() {

  const [page, setPage] = useState("Predict")
  

  const links =  [
    {
        title:"Find Patterns",
        link: "Predict"
    },
    {
        title:"Upload new DataSet",
        link: "NewDataSet"
    }
]

  return (
    <div className="App">
      <header className="App-header">
        <Navbar setPage={setPage} page={page} links={links} />
      </header>
        <Main page={page} setPage={setPage}/>
    </div>
  );
}

export default App;
