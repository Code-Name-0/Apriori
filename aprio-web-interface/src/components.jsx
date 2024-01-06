import './components.css'

// link structure: {title: str, link: str}
const Navbar = ({setPage, links, page}) => {
    return ( 
    <div className='navbar' >
        {links &&
            links.map((link, index) => {
                return <Navlink key={index} page={page} setPage={setPage} title={link.title}  link={link.link}/>
            })
            
        }
    </div> );
}

const Navlink = ({setPage, link, title, page}) => {
    return ( 
        <button className={link===page?'navlink navlink-active':'navlink'} onClick={()=>{setPage(link)}} >{title}</button>
   );
}


export {Navbar, Navlink}