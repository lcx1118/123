// import React, { useState } from 'react';
// import { useRouter } from 'next/router'; // 引入 useRouter 钩子
//
// function Register() {
//     const router = useRouter(); // 使用 useRouter
//     const [name, setName] = useState('');
//     const [email, setEmail] = useState('');
//     const [password, setPassword] = useState('');
//     const [error, setError] = useState('');
//
//     const handleSubmit = async (event) => {
//         event.preventDefault();
//         setError('');
//         const response = await fetch('/api/register', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ name, email, password }),
//         });
//         const data = await response.json();
//         if (!response.ok) {
//             setError(data.error || '注册失败');
//         } else {
//             alert('注册成功! 即将跳转到首页。');
//             router.push('/'); // 使用 router.push 方法重定向到主页
//         }
//     };
//
//     return (
//         <div>
//             <h1>注册</h1>
//             <form onSubmit={handleSubmit}>
//                 <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="输入姓名" required />
//                 <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="输入邮箱" required />
//                 <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="输入密码" required />
//                 <button type="submit">注册</button>
//                 {error && <p className="text-red-500 mt-2">{error}</p>}
//             </form>
//         </div>
//     );
// }
//
// export default Register;
// pages/register.js
import axios from 'axios';
import React, { useState } from 'react';
import { useRouter } from 'next/router';
export default function Register() {
    const [open, setOpen] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        phone_number: '',
        password: ''
    });
    const router = useRouter();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('http://localhost:8000/api/register/', formData);
            alert(res.data.message);
            if (res.status === 201) {
                router.push('/'); // Assuming '/welcome' is your welcome page route
            }
        } catch (error) {
            alert('Registration failed: ' + error.response.data.error);
        }
    };
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
                    <h2 className="mt-6 text-3xl font-extrabold text-center text-neutral-600">注册账户</h2>
                </div>

                <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
                    <div className="px-4 py-8 sm:px-10">
                        <form className="space-y-6" action="#"  onSubmit={handleSubmit}>
                            <div>
                                <label htmlFor="username" className="block text-sm font-medium text-gray-700"> 用户名 </label>
                                <div className="mt-1">
                                    <input id="username" name="username" type="text" autoComplete="username" onChange={handleChange} required className="block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-50 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-300"/>
                                </div>
                            </div>
                            <div>
                                <label htmlFor="email" className="block text-sm font-medium text-gray-700"> 邮 箱 </label>
                                <div className="mt-1">
                                    <input id="email" name="email" type="email" autoComplete="email" onChange={handleChange} required className="block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-50 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-300"/>
                                </div>
                            </div>
                            <div>
                                <label htmlFor="phone_number" className="block text-sm font-medium text-gray-700"> 手机号</label>
                                <div className="mt-1">
                                    <input id="phone_number" name="phone_number" type="text" autoComplete="phone_number" onChange={handleChange} required className="block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-50 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-300"/>
                                </div>
                            </div>

                            <div>
                                <label htmlFor="password"
                                       className="block text-sm font-medium text-gray-1000"> 密 码 </label>
                                <div className="mt-1">
                                    <input id="password" name="password" type="password" autoComplete="current-password"
                                           onChange={handleChange} required
                                           className="block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-50 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-300"/>
                                </div>
                            </div>

                            <div>
                                <button type="submit"
                                        className="flex items-center justify-center w-full px-10 py-4 text-base font-medium text-center text-white transition duration-500 ease-in-out transform bg-blue-600 rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">注册
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </section>
        </div>



    );

    // return (
    //     // <form onSubmit={handleSubmit}>
    //     //     <input type="text" name="username" placeholder="Username" onChange={handleChange} required />
    //     //     <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
    //     //     <input type="text" name="phone_number" placeholder="Phone Number" onChange={handleChange} required />
    //     //     <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
    //     //     <button type="submit">注册</button>
    //     // </form>
    //
    // );
}
