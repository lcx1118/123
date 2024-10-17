//
//
// import React, {useState, useEffect} from 'react';
// import Link from "next/link";
// function FeatureThree() {
//     const [open, setOpen] = useState(false);
//     const [images, setImages] = useState({ floorplan: [], core: [] });
//     const [selectedImages, setSelectedImages] = useState([]);
//     const [isModalOpen, setIsModalOpen] = useState(false);
//     const [generatedImageUrl, setGeneratedImageUrl] = useState('');
//     const [isLoading, setIsLoading] = useState(false);
//
//     useEffect(() => {
//         fetch('http://localhost:8000/api/images/')
//             .then(response => response.json())
//             .then(data => setImages(data))
//             .catch(error => console.error('Error fetching images:', error));
//     }, []);
//
//     const handleSelectImage = (url) => {
//         const newSelectedImages = selectedImages.includes(url) ?
//             selectedImages.filter(img => img !== url) :
//             [...selectedImages, url];
//         setSelectedImages(newSelectedImages);
//     };
//
//     const handleSubmit = () => {
//         setIsLoading(true);
//         fetch('http://localhost:8000/api/images/', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ selectedImages }),
//         })
//             .then(response => response.json())
//             .then(data => {
//                 setGeneratedImageUrl(data.imageUrl);
//                 setIsModalOpen(true);
//                 setIsLoading(false);
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//                 setIsLoading(false);
//             });
//     };
//
//    const downloadImage = async () => {
//         // 开始加载时设置为 true
//
//             const imageResponse = await fetch(`http://localhost:8000${generatedImageUrl}`); // 确保使用正确的完整URL
//             const blob = await imageResponse.blob(); // 获取blob
//             const downloadUrl = window.URL.createObjectURL(blob); // 创建下载链接
//             const link = document.createElement('a');
//             link.href = downloadUrl;
//             link.setAttribute('download', 'GeneratedImage.png'); // 设置下载的文件名
//             document.body.appendChild(link);
//             link.click();
//             link.parentNode.removeChild(link);
//             setIsModalOpen(false); // 关闭模态窗口
//
//     };
//
//
//     const closeModal = () => {
//         setIsModalOpen(false);
//     };
//
//
//
//     return (
//         <div>
//
//             <div className="flex justify-center mx-auto">
//                 <div x-data="{ open: false }"
//                      className="flex flex-col max-w-screen-xl p-5 mx-auto md:items-center md:justify-between md:flex-row md:px-6 lg:px-8">
//                     <div className="flex flex-row items-center justify-between lg:justify-start">
//                         <a className="text-lg font-bold tracking-tighter text-blue-600 transition duration-500 ease-in-out transform tracking-relaxed lg:pr-8"
//                            href="/groups/header/"> 智能设计平台 </a>
//                         <button className="rounded-lg md:hidden focus:outline-none focus:shadow-outline"
//                                 onClick={() => setOpen(!open)}>
//                             <svg fill="currentColor" viewBox="0 0 20 20" className="w-8 h-8">
//                                 {/* 更新路径和样式显示 */}
//                                 <path fillRule="evenodd"
//                                       d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM9 15a1 1 0 011-1h6a1 1 0 110 2h-6a1 1 0 01-1-1z"
//                                       clipRule="evenodd" style={{display: open ? 'none' : 'block'}}></path>
//                                 <path fillRule="evenodd"
//                                       d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
//                                       clipRule="evenodd" style={{display: open ? 'block' : 'none'}}></path>
//                             </svg>
//                         </button>
//                     </div>
//                     <nav
//                         className={`flex-col flex-grow ${open ? 'flex' : 'hidden'} md:flex md:justify-start md:flex-row`}>
//                         <ul className="space-y-2 list-none lg:space-y-0 lg:items-center lg:inline-flex">
//                             <li>
//                                 <a href="#"
//                                    className="px-2 lg:px-6 py-6 text-sm border-b-2 border-transparent hover:border-blue-600 leading-[22px] md:px-3 text-gray-500 hover:text-blue-500"> All <span
//                                     className="hidden lg:inline"> templates </span>
//                                 </a>
//                             </li>
//                             <li>
//                                 <a href="#"
//                                    className="px-2 lg:px-6 py-6 text-sm border-b-2 border-transparent leading-[22px] md:px-3 text-gray-500 hover:text-blue-500 hover:border-blue-600"> FAQ </a>
//                             </li>
//                             <li>
//                                 <a href="https://www.wickedtemplates.com/"
//                                    className="px-2 lg:px-6 py-6 text-sm border-b-2 border-transparent hover:border-blue-600 leading-[22px] md:px-3 text-gray-500 hover:text-blue-500"> Free <span
//                                     className="hidden lg:inline">Templates </span>
//                                 </a>
//                             </li>
//                         </ul>
//                     </nav>
//                 </div>
//             </div>
//              <section>
//                 <div className="relative items-center w-full py-24 mx-auto md:px-12 lg:px-16 max-w-7xl">
//                     <div className="px-5 overflow-hidden divide-y shadow-xl rounded-xl lg:px-0">
//                         {isLoading && (
//                             <div className="fixed inset-0 z-50 flex items-center justify-center">
//                                 <img src="http://localhost:8000/media/web_data/a.webp" alt="Loading"/>
//                             </div>
//                         )}
//
//                             <div className="flex flex-wrap items-end justify-start w-full bg-gray-50">
//                                 {images.floorplan.map((url, index) => (
//                                     <img
//                                         key={`floorplan-${index}`}
//                                         src={'http://localhost:8000/' + url}
//                                         alt={`Floorplan Image ${index}`}
//                                         style={{
//                                             opacity: selectedImages.includes(url) ? 1 : 0.5,
//                                             cursor: 'pointer',
//                                             width: '100px',
//                                             height: '100px'
//                                         }}
//                                         onClick={() => handleSelectImage(url)}
//                                     />
//                                 ))}
//                             </div>
//
//
//
//                             <div className="flex flex-wrap items-end justify-start w-full bg-gray-50">
//                                  {images.core.map((url, index) => (
//                                 <img
//                                     key={`core-${index}`}
//                                     src={'http://localhost:8000/' + url}
//                                     alt={`Core Image ${index}`}
//                                     style={{
//                                         opacity: selectedImages.includes(url) ? 1 : 0.5,
//                                         cursor: 'pointer',
//                                         width: '100px',
//                                         height: '100px'
//                                     }}
//                                     onClick={() => handleSelectImage(url)}
//                                 />
//                             ))}
//                             </div>
//
//
//                     </div>
//                 </div>
//             </section>
//             <div style={{ width: '200px', height: '30px', margin: '0 auto' }}>
//                 <button
//                     className="flex items-center justify-center w-full px-10 py-4 text-base font-medium text-center text-white transition duration-500 ease-in-out transform bg-blue-600 rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
//                     onClick={handleSubmit}>
//                     生成组合
//                 </button>
//             </div>
//              {/*模态窗口 */}
//             {isModalOpen && (
//                 <div className="fixed inset-0 z-50 overflow-auto bg-smoke-light flex">
//                     <div className="relative p-8 bg-white w-full max-w-md m-auto flex-col flex rounded-lg">
//                         <span className="absolute top-0 right-0 p-4">
//                             <button onClick={closeModal}>×</button>
//                         </span>
//                         <img src={'http://localhost:8000/'+ generatedImageUrl} alt="Generated"/>
//                         <button
//                             className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center"
//                             onClick={downloadImage}>
//                             下载组合
//                         </button>
//                     </div>
//                 </div>
//             )}
//
//
//         </div>
//
//     );
//
//
// }
//
// export default FeatureThree;
//





import React, {useState, useEffect} from 'react';
import Link from "next/link";
function FeatureThree() {
    const [open, setOpen] = useState(false);
    const [images, setImages] = useState({ floorplan: [], core: [] });
    const [selectedImages, setSelectedImages] = useState([]);
    // const [renderedImages, setRenderedImages] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [generatedImageUrl, setGeneratedImageUrl] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        fetch('http://localhost:8000/api/images/')
            .then(response => response.json())
            .then(data => setImages(data))
            .catch(error => console.error('Error fetching images:', error));
    }, []);
    const handleSelectImage = (url) => {
        // 为每个选择的图片生成一个唯一的ID
        const newImage = {
            url,
            id: Date.now() + Math.random() // 简单的唯一ID生成方法
        };
        setSelectedImages(prev => [...prev, newImage]); // 增加到选中图片的数组
        // setRenderedImages(prev => [...prev, newImage]); // 将新的对象添加到渲染数组
    };

    const handleRemoveImage = (id) => {
        // 通过唯一ID移除图片
        setSelectedImages(prev => prev.filter(img => img.id !== id));
    };
    // const handleSelectImage = (url) => {
    //     setSelectedImages(prev => [...prev, url]); // 允许多次选择同一图片
    //     setRenderedImages(prev => [...prev, url]); // 将选择的图片添加到渲染数组中
    // };
    // const handleRemoveImage = (id) => {
    //         setRenderedImages(prev => prev.filter(img => img.id !== id));
    //         setSelectedImages(prev => prev.filter((url, index) => `${url}-${index}` !== id));
    // };
    const handleSubmit = () => {
        setIsLoading(true);
        const imageUrls = selectedImages.map(img => img.url);
        fetch('http://localhost:8000/api/images/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selectedImages: imageUrls }),
        })
            .then(response => response.json())
            .then(data => {
                setGeneratedImageUrl(data.imageUrl);
                setIsModalOpen(true);
                setIsLoading(false);
            })
            .catch(error => {
                console.error('Error:', error);
                setIsLoading(false);
            });
    };

   const downloadImage = async () => {
        // 开始加载时设置为 true

            const imageResponse = await fetch(`http://localhost:8000/${generatedImageUrl}`); // 确保使用正确的完整URL
            const blob = await imageResponse.blob(); // 获取blob
            const downloadUrl = window.URL.createObjectURL(blob); // 创建下载链接
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.setAttribute('download', 'GeneratedImage.png'); // 设置下载的文件名
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
            setIsModalOpen(false); // 关闭模态窗口

    };


    const closeModal = () => {
        setIsModalOpen(false);
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
                <div className="relative items-center w-full py-24 mx-auto md:px-12 lg:px-16 max-w-7xl">
                    <div className="px-5 overflow-hidden divide-y shadow-xl rounded-xl lg:px-0">
                        {isLoading && (
                            <div className="fixed inset-0 z-50 flex items-center justify-center">
                                <img src="http://localhost:8000/media/web_data/a.webp" alt="Loading"/>
                            </div>
                        )}

                            <div className="flex flex-wrap items-end justify-start w-full bg-gray-50">
                                {images.floorplan.map((url, index) => (
                                     <img
                                    key={`floorplan-${index}`}
                                    src={'http://localhost:8000/' + url}
                                    alt={`Floorplan Image ${index}`}
                                    style={{ opacity: 1, cursor: 'pointer', width: '100px', height: '100px' ,margin: '5px' }}
                                    onClick={() => handleSelectImage(url)}
                                />
                                ))}
                            </div>



                            <div className="flex flex-wrap items-end justify-start w-full bg-gray-50">
                                 {images.core.map((url, index) => (
                                <img
                                    key={`core-${index}`}
                                    src={'http://localhost:8000/' + url}
                                    alt={`Core Image ${index}`}
                                    style={{ opacity: 1, cursor: 'pointer', width: '100px', height: '100px',margin: '5px'  }}
                                    onClick={() => handleSelectImage(url)}
                                />
                            ))}
                            </div>

                            <div className="flex flex-wrap items-end justify-start w-full bg-lightblue">
                                {selectedImages.map(image => (
                                    <img
                                        key={image.id} // 使用唯一ID作为key
                                        src={'http://localhost:8000/' + image.url}
                                        alt="Selected Image"
                                        style={{ width: '100px', height: '100px' ,margin: '5px' }}
                                        onClick={() => handleRemoveImage(image.id)} // 传递唯一ID到处理函数
                                    />
                                ))}
                            </div>


                    </div>
                </div>
            </section>
            <div style={{ width: '200px', height: '30px', margin: '0 auto' }}>
                <button
                    className="flex items-center justify-center w-full px-10 py-4 text-base font-medium text-center text-white transition duration-500 ease-in-out transform bg-blue-600 rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    onClick={handleSubmit}>
                    生成组合
                </button>
            </div>
             {/*模态窗口 */}
            {isModalOpen && (
                <div className="fixed inset-0 z-50 overflow-auto bg-smoke-light flex">
                    <div className="relative p-8 bg-white w-full max-w-md m-auto flex-col flex rounded-lg">
                        <span className="absolute top-0 right-0 p-4">
                            <button onClick={closeModal}>×</button>
                        </span>
                        <img src={'http://localhost:8000/'+ generatedImageUrl} alt="Generated"/>
                        <button
                            className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center"
                            onClick={downloadImage}>
                            下载组合
                        </button>
                    </div>
                </div>
            )}


        </div>

    );


}

export default FeatureThree;

