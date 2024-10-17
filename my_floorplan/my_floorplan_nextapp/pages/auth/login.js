//
// import axios from 'axios';
// import { useState } from 'react';
// import { useRouter } from 'next/router';
// export default function Login() {
//     const [formData, setFormData] = useState({
//         email_or_phone: '',
//         password: ''
//     });
//     const [error, setError] = useState('');
//     const router = useRouter();
//
//     const handleChange = (e) => {
//         setFormData({ ...formData, [e.target.name]: e.target.value });
//     };
//
//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         try {
//             const res = await axios.post('http://localhost:8000/api/login/', formData);
//              if (res.data.token) {
//                 localStorage.setItem('token', res.data.token);  // Save token
//                 router.push('/auth/features'); // Assuming '/features' is your features selection page
//             }
//             // Redirect to another page or save the token etc.
//         } catch (error) {
//             alert("Login failed: " + error.response.data.error);
//         }
//     };
//
//     return (
//         <form onSubmit={handleSubmit}>
//             <input type="text" name="email_or_phone" placeholder="Email or Phone" onChange={handleChange} required />
//             <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
//             <button type="submit">登录</button>
//         </form>
//     );
// }

import axios from 'axios';
import React, { useState } from 'react';
import { useRouter } from 'next/router';
export default function Login() {
    const [formData, setFormData] = useState({
        email_or_phone: '',
        password: ''
    });
    const [open, setOpen] = useState(false);
    const [error, setError] = useState('');
    const router = useRouter();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('http://localhost:8000/api/login/', formData);
             if (res.data.token) {
                localStorage.setItem('token', res.data.token);  // Save token
                router.push('/auth/features'); // Assuming '/features' is your features selection page
            }
            // Redirect to another page or save the token etc.
        } catch (error) {
            alert("Login failed: " + error.response.data.error);
        }
    };

            // <input type="text" name="email_or_phone" placeholder="Email or Phone" onChange={handleChange} required />
            // <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
            // <button type="submit">登录</button>
    return (
        <div>
        <div className="flex justify-center mx-auto">
                <div x-data="{ open: false }"
                     className="flex flex-col max-w-screen-xl p-5 mx-auto md:items-center md:justify-between md:flex-row md:px-6 lg:px-8">
                    <div className="flex flex-row items-center justify-between lg:justify-start">
                        <a className="text-lg font-bold tracking-tighter text-blue-600 transition duration-500 ease-in-out transform tracking-relaxed lg:pr-8"
                           href="#"> 智能设计平台 </a>
                        <button className="rounded-lg md:hidden focus:outline-none focus:shadow-outline"
                                onClick={() => setOpen(!open)}>
                            <svg fill="currentColor" viewBox="0 0 20 20" className="w-8 h-8">
                                {/* 更新路径和样式显示 */}
                                <path fillRule="evenodd"
                                      d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM9 15a1 1 0 011-1h6a1 1 0 110 2h-6a1 1 0 01-1-1z"
                                      clipRule="evenodd" style={{display: open ? 'none' : 'block'}}></path>
                                <path fillRule="evenodd"
                                      d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                      clipRule="evenodd" style={{display: open ? 'block' : 'none'}}></path>
                            </svg>
                        </button>
                    </div>
                    <nav
                        className={`flex-col flex-grow ${open ? 'flex' : 'hidden'} md:flex md:justify-start md:flex-row`}>
                        <ul className="space-y-2 list-none lg:space-y-0 lg:items-center lg:inline-flex">
                            <li>
                                <a href="#"
                                   className="px-2 lg:px-6 py-6 text-sm border-b-2 border-transparent hover:border-blue-600 leading-[22px] md:px-3 text-gray-500 hover:text-blue-500"> All <span
                                    className="hidden lg:inline"> templates </span>
                                </a>
                            </li>
                            <li>
                                <a href="#"
                                   className="px-2 lg:px-6 py-6 text-sm border-b-2 border-transparent leading-[22px] md:px-3 text-gray-500 hover:text-blue-500 hover:border-blue-600"> FAQ </a>
                            </li>
                            <li>
                                <a href="#"
                                   className="px-2 lg:px-6 py-6 text-sm border-b-2 border-transparent hover:border-blue-600 leading-[22px] md:px-3 text-gray-500 hover:text-blue-500"> Free <span
                                    className="hidden lg:inline">Templates </span>
                                </a>
                            </li>
                        </ul>
                    </nav>
                </div>
            </div>

        <section>
            <div className="flex flex-col justify-center min- py-12 sm:px-6 lg:px-8">
                <div className="sm:mx-auto sm:w-full sm:max-w-md">
                    <h2 className="mt-6 text-3xl font-extrabold text-center text-neutral-600">登录您的账户</h2>
                </div>

                <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
                    <div className="px-4 py-8 sm:px-10">
                        <form className="space-y-6" action="#" method="POST"  onSubmit={handleSubmit}>
                            <div>
                                <label htmlFor="name" className="block text-sm font-medium text-gray-700"> 用户名 </label>
                                <div className="mt-1">
                                    <input id="name" name="name" type="text" autoComplete="name" onChange={handleChange} required className="block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-50 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-300"/>
                             </div>
                            </div>

                            <div>
                                <label htmlFor="password"
                                       className="block text-sm font-medium text-gray-1000"> 密码 </label>
                                <div className="mt-1">
                                    <input id="password" name="password" type="password" autoComplete="current-password"
                                           onChange={handleChange} required
                                           className="block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-50 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-300"/>
                                </div>
                            </div>

                            <div>
                                <button type="submit"
                                        className="flex items-center justify-center w-full px-10 py-4 text-base font-medium text-center text-white transition duration-500 ease-in-out transform bg-blue-600 rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">登录
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </section>
        </div>
        // <form onSubmit={handleSubmit}>
        //
        // </form>

    );
}
