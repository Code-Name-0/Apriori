import axios from "axios";
import { api } from "./env";
import { useEffect, useState } from "react";
import Select from 'react-select';
import { setSelectionRange } from "@testing-library/user-event/dist/utils";


const Predict = () => {
    const [products, setProducts] = useState([])
    const [sample, setSample] = useState([])
    const [predictions, setPredictions] = useState([])

    const  get_prediction = async (sample) => {
      console.log('getting prediction')
      const prediction = await axios.post(api+"Predict", {sample: sample})
      setPredictions(prediction.data.sort((a, b) => {return b.lift - a.lift} ))
    }

    const get_products = async () => {
        const response = await axios.get(api + "get_products");
        return response.data;
      };
    
      useEffect(() => {
        const fetchData = async () => {
          try {
            const prods = await get_products();
            setProducts(prods)
          } catch (error) {
            console.error('Error fetching data:', error);
          }
        };
    
        fetchData();
      }, []);

      useEffect(()=>{
        if(sample.length !== 0)
          get_prediction(sample)
        else{
          setPredictions([])
        }
      }, [sample])


  const removeProductFromSample = (product) => {
    if(products.includes(product) && sample.includes(product)){
      setSample(sample.filter((p) => {
        return p !== product
      }))
    }
  }

  console.log(predictions)

    return ( 
        <div className="predict-container" >

            <div className="basket-container">
              <div className="search-container">
                <Search products={products} sample={sample} setSample={setSample} />  
                
              </div>

              <div className="basket">
                {sample.map((product, index)=> {
                    return <SampleProduct removeProductFromSample={removeProductFromSample} product={product} key={index} />
                })}
              </div>
              
              {/* { sample.length !== 0 && <button className="predict-btn" onClick={()=>{get_prediction(sample)}} >Predict</button>} */}
            </div>
            <div className="results-container">
                {predictions && predictions.length !== 0 &&
                  predictions.map((pred, index) => {
                    return <Prediction key={index} prediction={pred}/>
                  })
                }
            </div>
            {/* <h1>Predict Page</h1>
            
             */}
        </div>
     );
}
 
export default Predict;

const Prediction = ({prediction}) => {
  return (
    <div className="prediction-container">
      {prediction.consequent.map((cons, index) => {
        return <div key={index} className="pred">
          <div className="cons">
            {cons}
          </div>
        </div>
      })}
      <div className="metrics">
        <div className="confidence">
          Confidence: {prediction.confidence}
        </div>
        <div className="lift">
          Lift: {prediction.lift}
        </div>
      </div>
    </div>
  )
}


const Search = ({sample, setSample, products}) => {
    const suggsPageSize = 5
    const [sampleSearchValue, setSampleSearchValue] = useState("")
    const [suggestions, setSuggestions] = useState([])
    const [maxPage, setMaxPage] = useState(10)
    const updateSample = (value) => {
        if( products.includes(value) && !sample.includes(value)){
            setSample([...sample, value].sort((a, b) => a.length - b.length))
        }
    }

    
    const updateSuggs = (prod) => {
      let suggs
      if(prod.length === 0){
        suggs = []
      }
      else{
        suggs = products.filter(p => p.toLowerCase().includes(prod.toLowerCase())).sort((a, b) => a.length - b.length)
        
        
      }
      setSuggestions(suggs)
    }
    useEffect(()=>{
      setMaxPage(Math.floor(suggestions.length / suggsPageSize))
    },[suggestions])
    


    const onSearchChange = (e) => {
      setSampleSearchValue(e.target.value); 
      updateSuggs(e.target.value); 
      setSuggsPage(1)
    }


    const [suggsPage, setSuggsPage] = useState(1)
    // console.log(suggestions)
    return ( 
        <div className="search" >
            <input className="search-input" placeholder="Search" value={sampleSearchValue} onChange={(e)=>{onSearchChange(e)}} />
            {/* <button className="add-btn" onClick={updateSample(sampleSearchValue)} >Add </button> */}
            <div className="suggs-container">
            {
            suggestions &&
            suggestions.length !== 0 &&
            
                  <>
                  <div className="suggs">
                  {suggestions.slice(suggsPageSize*(suggsPage - 1), suggsPageSize*suggsPage).map((sug, index) => {
                      return <div className="sugg" onClick={()=>{updateSample(sug)}} key={index}> {sug} </div>
                  })}
                  </div>

                  {maxPage > 1 &&
                    <div className="suggs-btns">
                        <button className="prev-btn" onClick={()=>{if (suggsPage > 1) setSuggsPage(suggsPage - 1)}} >Previous</button>
                        <h3>{suggsPage}</h3>
                        <button className="next-btn" onClick={()=>{if (suggsPage < maxPage) setSuggsPage(suggsPage + 1)}} >Next</button>
                    </div>}
                    </>

            
        }
                </div>
        </div>
        
        
     );
}
 
const SampleProduct = ({product,removeProductFromSample}) => {


  return (
    <div className="sampleProduct">
      <div className="name">{product}</div>
      <div onClick={()=>{removeProductFromSample(product)}} className="remove">
        <div className="line1" ></div>
        <div className="line2" ></div>
      </div>
    </div>
  )
}
