import { Button } from '@nextui-org/react';
import React, {useState} from "react";

export default function Home() {
    const [open, setOpen] = useState(false);
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
          <div className="relative items-center w-full px-5 py-12 mx-auto md:px-12 lg:px-16 max-w-7xl lg:py-24">
              <div className="flex w-full mx-auto text-left">
                  <div className="relative inline-flex items-center mx-auto align-middle">
                      <div className="text-center" >
                          <h1 className="max-w-5xl text-2xl font-bold leading-none tracking-tighter text-neutral-600 md:text-5xl lg:text-6xl lg:max-w-7xl">
                              欢迎来到高层智能设计云平台!
                          </h1>
                          <p className="max-w-xl mx-auto mt-8 text-base leading-relaxed text-gray-500">一键生成自己的户型图&amp;智能组合现有户型和交通核</p>

                          <div className="flex justify-center w-full max-w-2xl gap-2 mx-auto mt-6">
                              <div className="mt-3 rounded-lg sm:mt-0">
                                  <button onClick={() => window.location.href = '/auth/register'} shadow auto color="gradient"
                                      className="items-center block px-5 lg:px-10 py-3.5 text-base font-medium text-center text-blue-600 transition duration-500 ease-in-out transform border-2 border-white shadow-md rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500">
                                      注册
                                  </button>
                              </div>
                              <div className="mt-3 rounded-lg sm:mt-0 sm:ml-3">
                                  <button  onClick={() => window.location.href = '/auth/login'} shadow auto color="gradient"
                                      className="px-5 py-4 text-base font-medium text-center text-white transition duration-500 ease-in-out transform bg-blue-600 lg:px-10 rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                      登录
                                  </button>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>
              <section id="intro">
                  <div
                      className="flex flex-col items-center justify-center pt-24 mx-auto rounded-lg lg:px-10 max-w-7xl">
                      <img className="object-cover object-center w-full rounded-xl" alt="hero"
                           src="http://localhost:8000/media/web_data/background1.png"/>

                  </div>
              </section>
          </div>
      </section></div>

  );
}
