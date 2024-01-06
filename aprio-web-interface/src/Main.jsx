
import { Navbar, Navlink } from './components';
import Predict from './Predict';
import NewDS from './NewDS';
import './Main.css'


const Main = ({page, setPage}) => {


    return ( <div className='main-container' >
        {page == "Predict" ? <Predict/> : <NewDS/>}
        
    </div> );
}
 


 
 


export default Main;