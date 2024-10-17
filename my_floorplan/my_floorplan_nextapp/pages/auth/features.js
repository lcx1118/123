import Link from 'next/link';
// import React from 'react';
import React, { useState } from 'react';
import {Button} from "@nextui-org/react";

function Features() {
    const [open, setOpen] = useState(false);
    return (
        <div>
            {/* 新增的上边栏代码 */}
            <div className="flex justify-center mx-auto">
                <div x-data="{ open: false }" className="flex flex-col max-w-screen-xl p-5 mx-auto md:items-center md:justify-between md:flex-row md:px-6 lg:px-8">
                    <div className="flex flex-row items-center justify-between lg:justify-start">
                        <a className="text-lg font-bold tracking-tighter text-blue-600 transition duration-500 ease-in-out transform tracking-relaxed lg:pr-8" href="#"> 智能设计平台 </a>
                        <button className="rounded-lg md:hidden focus:outline-none focus:shadow-outline" onClick={() => setOpen(!open)}>
                            <svg fill="currentColor" viewBox="0 0 20 20" className="w-8 h-8">
                                {/* 更新路径和样式显示 */}
                                <path fillRule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM9 15a1 1 0 011-1h6a1 1 0 110 2h-6a1 1 0 01-1-1z" clipRule="evenodd" style={{ display: open ? 'none' : 'block' }}></path>
                                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" style={{ display: open ? 'block' : 'none' }}></path>
                            </svg>
                        </button>
                    </div>
                    <nav className={`flex-col flex-grow ${open ? 'flex' : 'hidden'} md:flex md:justify-start md:flex-row`}>
                        <ul className="space-y-2 list-none lg:space-y-0 lg:items-center lg:inline-flex">
                            <li>
                                <a href="#" className="px-2 lg:px-6 py-6 text-sm border-b-2 border-transparent hover:border-blue-600 leading-[22px] md:px-3 text-gray-500 hover:text-blue-500"> All <span className="hidden lg:inline"> templates </span>
                                </a>
                            </li>
                            <li>
                                <a href="#" className="px-2 lg:px-6 py-6 text-sm border-b-2 border-transparent leading-[22px] md:px-3 text-gray-500 hover:text-blue-500 hover:border-blue-600"> FAQ </a>
                            </li>
                            <li>
                                <a href="#" className="px-2 lg:px-6 py-6 text-sm border-b-2 border-transparent hover:border-blue-600 leading-[22px] md:px-3 text-gray-500 hover:text-blue-500"> Free <span className="hidden lg:inline">Templates </span>
                                </a>
                            </li>
                        </ul>
                    </nav>
                </div>
            </div>

        <section className="">

            <div className="flex justify-center items-center min-h-screen">

              <Link href="/auth/features1">

                        <div className="flex w-full">
                            <div className="relative flex flex-col items-start m-1 transition duration-300 ease-in-out delay-150 transform bg-white shadow-2xl rounded-xl md:w-80 md:-ml-16 md:hover:-translate-x-16 md:hover:-translate-y-8">
                                <img className="object-cover object-center w-full rounded-t-xl lg:h-48 md:h-36" src="http://localhost:8000/media/web_data/features11.png" alt="blog"/>
                                <div className="px-6 py-8">
                                    <h4 className="mt-4 text-2xl font-semibold text-neutral-600">进入生成布局</h4>
                                    <p className="mt-4 text-base font-normal text-gray-500 leading-relax">用户通过上传理想户型图和轮廓，生成符合自己需求的户型图
                                        <br className="hidden lg:block"/>
                                        <br className="hidden lg:block"/>
                                        <br className="hidden lg:block"/>
                                        <br className="hidden lg:block"/>
                                    </p>
                                </div>
                            </div>
                        </div>

              </Link>


                <Link href="/auth/FeatureThree">
                    <div className="flex w-full">
                        <div className="relative flex flex-col items-start m-1 transition duration-300 ease-in-out delay-150 transform bg-white shadow-2xl rounded-xl md:w-80 md:-ml-16 md:hover:-translate-x-16 md:hover:-translate-y-8">
                            <img className="object-cover object-center w-full rounded-t-xl lg:h-48 md:h-36"
                                 src="http://localhost:8000/media/web_data/features2.png" alt="blog"/>
                                <div className="px-6 py-8">
                                    <h4 className="mt-4 text-2xl font-semibold text-neutral-600">
                                        <span className="">组合户型和交通核</span>
                                    </h4>
                                    <p className="mt-4 text-base font-normal text-gray-500 leading-relax">用户选择户型以及交通单元，生成符合需求的单元设计图
                                        <br className="hidden lg:block"/>
                                        <br className="hidden lg:block"/>
                                        <br className="hidden lg:block"/>
                                        <br className="hidden lg:block"/>
                                    </p>
                                </div>
                        </div>
                    </div>
                </Link>


                <a href="">
                    <div className="flex w-full">
                        <div
                            className="relative flex flex-col items-start m-1 transition duration-300 ease-in-out delay-150 transform bg-white shadow-2xl rounded-xl md:w-80 md:-ml-16 md:hover:-translate-x-16 md:hover:-translate-y-8">
                                <img className="object-cover object-center w-full rounded-t-xl lg:h-48 md:h-36"
                                     src="http://localhost:8000/media/web_data/card3.png" alt="blog"/>
                                <div className="px-6 py-8">
                                    <h4 className="mt-4 text-2xl font-semibold text-neutral-600">
                                        <span className="">敬请期待.....</span>
                                    </h4>
                                    <p className="mt-4 text-base font-normal text-gray-500 leading-relax">
                                        <br className="hidden lg:block"/>
                                        <br className="hidden lg:block"/>
                                        <br className="hidden lg:block"/>
                                        <br className="hidden lg:block"/>
                                        <br className="hidden lg:block"/>
                                    </p>
                                </div>
                        </div>
                    </div>
                </a>


            </div>
        </section>
    </div>
    );
}

export default Features;
