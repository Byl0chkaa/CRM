import React from 'react';
import {useForm} from "react-hook-form";
import {useNavigate} from "react-router-dom"
import {authService} from "../../services/authService";
import './LoginPage.css'

const LoginPage = () => {
    const {register, handleSubmit} = useForm();
    const navigate = useNavigate();
    const onSubmit = async (user) => {
        await authService.login(user)
        navigate('/orders')
    }
    return (
        <div className="login-page-container">
            <form onSubmit={handleSubmit(onSubmit)}>
                <div className={'form-data'}>
                    <label htmlFor="">Email</label>
                    <input type="text" placeholder={'Email'} {...register('email')}/>
                    <label htmlFor="">Password</label>
                    <input type="password" placeholder={'Password'} {...register('password')}/>
                    <button>LOGIN</button>
                </div>
            </form>
        </div>
    );
};

export default LoginPage;