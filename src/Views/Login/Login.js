import './Login.scss'
import { useState } from 'react';
import logo from '../../assets/logo2.png'

const Login = props => {

    const [userLocal, setUserLocal] = useState('')
    const [pwd, setPwd] = useState('');
    const [authNum, setAuthNum] = useState(1);

    const handleSubmitFirst = e => {
        e.preventDefault();
        if (userLocal && pwd) {
            //TODO: check credentials here
            if(1) { //if credentials valid
                setAuthNum(2);
                localStorage.setItem('user', userLocal);
                props.setUser(userLocal);
                setUserLocal('');
                setPwd('');
            } else {
                console.log("Credentials invalid.")
            }
        } else {
            console.log('Please enter username and password.')
        }
    }

    const handleSubmitSecond = e => {
        e.preventDefault();
        //TODO: check QR code here
        if(1) { //if code valid
            props.setIsLoggedIn(true);
            props.setIsLogging(false);
        } else {
            console.log("Code invalid.")
        }
    }

    return (
        <div className="Login">
            <img src={logo} alt='logo' className='logo'/>
            {authNum === 1 && 
                <div className="login-container">    
                    <h2 className="login-header">Login</h2>
                    <form onSubmit={ handleSubmitFirst }>
                        <label className="login-label">
                            User
                        </label>
                        <input value={ userLocal } type="text" className="user-input" onChange={(e) => setUserLocal(e.target.value)} />
                        <label className="pwd-label">
                            Password
                        </label>
                        <input value={ pwd } type="password" className="pwd-input" onChange={(e) => setPwd(e.target.value)} />
                        <input type="submit" className="submit" value="Submit" />
                    </form>
                </div>
            }
            {authNum === 2 && 
                <div className="login-container">
                    <form onSubmit={ handleSubmitSecond }>
                        <h2 className="login-header">QR code placeholder</h2>
                        <input type="submit" className="submit" value="Submit" />
                    </form>
                </div>
            }
        </div>
    );
}
 
export default Login;