import './Login.scss'
import { useEffect, useState } from 'react';
import logo from '../../assets/logo2.png'

const Login = props => {

    const [userLocal, setUserLocal] = useState('')
    const [pwd, setPwd] = useState('');
    const [otp, setOtp] = useState('');
    const [authNum, setAuthNum] = useState(1);
    const [checked, setChecked] = useState(false);
    const [errorText, setErrorText] = useState('');
    const [qrCode, setQrCode] = useState();

    const handleSubmitFirst = e => {
        e.preventDefault();
        if (userLocal && pwd) {

            fetch('http://localhost:5000/login').then(
                res => res.json()
              ).then(
                receivedData => setQrCode(receivedData)
              )

            fetch('http://localhost:5000/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    'username': userLocal,
                    'password': pwd,
                    'otp_verification': checked,
                    'otp': otp
                })
            }).then(
                    res => {
                        res.json();
                        if(res.status === 201 || res.status === 202) {
                            props.setUser(userLocal);
                            setUserLocal('');
                            setPwd('');
                            setErrorText('');
                            if(res.status === 202) {
                                setAuthNum(2);
                            } else {
                                props.setIsLoggedIn(true);
                                props.setIsLogging(false);
                            }
                        } else {
                            switch (res.status) {
                                case 401:
                                    setErrorText('Wrong credentials');
                                    break;
                                case 402:
                                    setErrorText('Wrong token');
                                    break;
                                case 403:
                                    setErrorText("That's not the first time you're logging");
                                    break;
                                case 404:
                                    setErrorText('Wrong password');
                                    break;
                            }
                        }                        
                    }
                ).catch(
                    error => console.log(error)
                )
        } else {
            setErrorText('Please enter username and password.');
        }
    }

    useEffect(() => {
        if(authNum === 2) {
            fetch('http://localhost:5000/getqr').then(
                res => res.json()
              ).then(
                receivedData => setQrCode(receivedData)
              )
        }
    },[authNum])

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

    const handleChange = () => {
        setChecked(current => !current);
    }

    return (
        <div className="Login">
            <img src={logo} alt='logo' className='logo'/>
            {authNum === 1 && 
                <div className="login-container">    
                    <h2 className="login-header">Login</h2>
                    {errorText!=='' && <p className='alert'>{errorText}</p>}
                    <form onSubmit={ handleSubmitFirst }>
                        <label className="login-label">
                            User
                        </label>
                        <input value={ userLocal } type="text" className="user-input" onChange={(e) => setUserLocal(e.target.value)} />
                        <label className="pwd-label">
                            Password
                        </label>
                        <input value={ pwd } type="password" className="pwd-input" onChange={(e) => setPwd(e.target.value)} />
                        <label className={!checked ? "otp-label visible" : "otp-label invisible"}>
                            OTP
                        </label>
                        <input value={ otp } type="text" className={!checked ? "otp-input visible" : "otp-input invisible"} onChange={(e) => setOtp(e.target.value)} />
                        <div className="otp-checkbox">
                            <input type="checkbox" checked={checked} onChange={handleChange}/>
                            <p>Logging for the first time</p>
                        </div>
                        <input type="submit" className="submit" value="Submit" />
                    </form>
                </div>
            }
            {authNum === 2 && 
                <div className="login-container">
                    <form onSubmit={ handleSubmitSecond }>
                        <img className='qrcode' src={qrCode} />
                        <input type="submit" className="submit" value="Submit" />
                    </form>
                </div>
            }
        </div>
    );
}
 
export default Login;