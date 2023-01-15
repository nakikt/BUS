import './Header.scss'
import logo from '../../assets/logo2.png'

const Header = props => {
    
    const handleClick = () => {
        if(props.isLoggedIn) {
            props.setIsLoggedIn(false);
            props.setUser('');
        } else {
            props.setIsLogging(true);
        }
        
    }

    return (
        <div className="Header">
            <div className="container">
                <div className="inner">
                    <img src={logo} alt='logo' className='logo'/>
                    {props.user!=='' && <h2 className="greeting">Welcome, {props.user}!</h2>}
                    <div className="btn">
                        <button className="login" onClick={handleClick}>
                            {props.isLoggedIn ? "Log out" : "Login"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
 
export default Header;