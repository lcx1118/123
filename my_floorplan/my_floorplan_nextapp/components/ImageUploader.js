
// import React, { useState, useRef, useEffect } from 'react';
//
// function ImageUploader() {
//     const [image, setImage] = useState(null);
//     const [imageUrl, setImageUrl] = useState('');
//     const [radius, setRadius] = useState('');
//     const [selectedColor, setSelectedColor] = useState('');
//     const [circles, setCircles] = useState([]);
//     const canvasRef = useRef(null);
//     const fileInputRef = useRef(null); // 添加引用
//
//     const handleImageChange = (event) => {
//         const file = event.target.files[0];
//         setImage(file);
//         setImageUrl(URL.createObjectURL(file));
//         setCircles([]); // 清空之前的圆圈信息
//     };
//
//     const handleRadiusChange = (event) => {
//         setRadius(event.target.value);
//     };
//
//     const handleColorClick = (color) => {
//         setSelectedColor(color); // 单选颜色
//     };
//
//     const handleUpload = async () => {
//         const canvas = canvasRef.current;
//         if (!canvas) return;
//
//         canvas.toBlob(async (blob) => {
//             const formData = new FormData();
//             formData.append('file', blob, 'image_with_circles.png');
//
//             const response = await fetch('http://localhost:8000/api/upload/', {
//                 method: 'POST',
//                 body: formData,
//             });
//             const data = await response.json();
//
//             alert(data.message); // 可以展示来自后端的消息，例如文件处理位置
//         });
//     };
//
//     const handleCanvasClick = (event) => {
//         if (!selectedColor || radius === '') return;
//
//         const canvas = canvasRef.current;
//         const rect = canvas.getBoundingClientRect();
//         const x = event.clientX - rect.left;
//         const y = event.clientY - rect.top;
//         const newCircle = { x, y, radius: parseInt(radius), color: selectedColor };
//
//         setCircles(prev => [...prev, newCircle]);
//     };
//
//     const removeCircle = (index) => {
//         setCircles(prev => prev.filter((_, i) => i !== index));
//     };
//
//     useEffect(() => {
//         const canvas = canvasRef.current;
//         const ctx = canvas.getContext('2d');
//
//         const img = new Image();
//         img.src = imageUrl;
//         img.onload = () => {
//             canvas.width = 256;
//             canvas.height = 256;
//             ctx.clearRect(0, 0, canvas.width, canvas.height);
//             ctx.drawImage(img, 0, 0, 256, 256);
//             circles.forEach(circle => {
//                 ctx.beginPath();
//                 ctx.arc(circle.x, circle.y, circle.radius, 0, Math.PI * 2);
//                 ctx.fillStyle = circle.color;
//                 ctx.fill();
//             });
//         };
//     }, [imageUrl, circles]);
//
//     return (
//         <div className="flex flex-col items-center w-full min-h-screen p-5">
//             <div className="grid w-full max-w-7xl gap-12 lg:grid-cols-3" style={{height:500}}>
//                 <div className="p-6 bg-white rounded-3xl shadow-lg dark:bg-neutral-700">
//                     <div className="text-center">
//                         <h1 className="mb-8 text-2xl font-semibold text-neutral-600 lg:text-3xl">选择颜色:</h1>
//                         <div className="flex justify-center space-x-2 mb-4">
//                             {['red', 'green', 'blue', 'yellow', 'purple'].map(color => (
//                                 <button
//                                     key={color}
//                                     className={`w-8 h-8 rounded-full ${selectedColor === color ? 'ring-2 ring-offset-2 ring-blue-500' : ''}`}
//                                     style={{ backgroundColor: color }}
//                                     onClick={() => handleColorClick(color)}
//                                 />
//                             ))}
//                         </div>
//                         <input
//                             type="number"
//                             value={radius} onChange={handleRadiusChange}
//                             className="block w-full px-3 py-2 mb-4 border rounded-md dark:bg-transparent dark:border-white/10"
//                             placeholder="半径"
//                         />
//                     </div>
//                     <div className="overflow-y-auto max-h-60">
//                         {circles.map((circle, index) => (
//                             <div key={index} className="flex items-center justify-between p-2">
//                                 <span>圆 - 颜色: {circle.color} 半径: {circle.radius}</span>
//                                 <button className="text-red-500" onClick={() => removeCircle(index)}>删除</button>
//                             </div>
//                         ))}
//                     </div>
//                 </div>
//                 <div className="p-6 bg-white rounded-3xl shadow-lg dark:bg-neutral-700">
//                     <div className="flex items-center justify-center h-full">
//                         <canvas ref={canvasRef} onClick={handleCanvasClick} />
//                     </div>
//                 </div>
//                 <div className="p-6 bg-white rounded-3xl shadow-lg dark:bg-neutral-700">
//                     {/* 这里可以添加更多内容 */}
//                 </div>
//             </div>
//             <div className="flex justify-center w-full mt-10 space-x-4">
//                 <button
//                     className="px-5 py-4 text-base font-medium text-white transition duration-500 ease-in-out transform bg-blue-600 rounded-xl lg:px-10 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
//                     onClick={() => fileInputRef.current.click()}
//                 >
//                     选择图像
//                 </button>
//                 <input
//                     type="file"
//                     ref={fileInputRef} // 关联引用
//                     style={{ display: 'none' }} // 隐藏文件输入框
//                     onChange={handleImageChange}
//                 />
//                 <button
//                     className="px-5 py-4 text-base font-medium text-white transition duration-500 ease-in-out transform bg-blue-600 rounded-xl lg:px-10 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
//                     onClick={handleUpload}
//                 >
//                     上传图像
//                 </button>
//             </div>
//         </div>
//     );
// }
//
// export default ImageUploader;

import React, { useState, useRef, useEffect } from 'react';

function ImageUploader() {
    const [image, setImage] = useState(null);
    const [imageUrl, setImageUrl] = useState('');
    const [generatedImageUrl, setGeneratedImageUrl] = useState('');
    const [radius, setRadius] = useState('');
    const [selectedColor, setSelectedColor] = useState('');
    const [circles, setCircles] = useState([]);
    const canvasRef = useRef(null);
    const fileInputRef = useRef(null); // 添加引用

    const colors = [
        { color: 'rgb(171, 244, 253)', label: '卧室' },
        { color: 'rgb(229, 242, 244)', label: '客厅' },
        { color: 'rgb(214, 216, 234)', label: '厨房' },
        { color: 'rgb(252, 233, 205)', label: '卫生间' },
        { color: 'rgb(135, 216, 208)', label: '阳台' }
    ];

    const handleImageChange = (event) => {
        const file = event.target.files[0];
        setImage(file);
        setImageUrl(URL.createObjectURL(file));
        setCircles([]); // 清空之前的圆圈信息
    };

    const handleRadiusChange = (event) => {
        setRadius(event.target.value);
    };

    const handleColorClick = (color) => {
        setSelectedColor(color); // 单选颜色
    };

    const handleUpload = async () => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        canvas.toBlob(async (blob) => {
            const formData = new FormData();
            formData.append('file', blob, 'image_with_circles.png');

            const response = await fetch('http://localhost:8000/api/upload/', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            if (data.image_url) {
                  setGeneratedImageUrl(data.image_url); // 设置生成图像的URL
            }


             // 可以展示来自后端的消息，例如文件处理位置
        });
    };
    const handleUpload2 = async () => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        canvas.toBlob(async (blob) => {
            const formData = new FormData();
            formData.append('file', blob, 'image_with_circles.png');

            const response = await fetch('http://localhost:8000/api/upload2/', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            if (data.image_url) {
                  setGeneratedImageUrl(data.image_url); // 设置生成图像的URL
            }


             // 可以展示来自后端的消息，例如文件处理位置
        });
    };

    const handleCanvasClick = (event) => {
        if (!selectedColor || radius === '') return;

        const canvas = canvasRef.current;
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const selectedRoom = colors.find(c => c.color === selectedColor);
        const newCircle = { x, y, radius: parseInt(radius), label: selectedRoom.label, color: selectedColor };

        setCircles(prev => [...prev, newCircle]);
    };

    const removeCircle = (index) => {
        setCircles(prev => prev.filter((_, i) => i !== index));
    };

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        const img = new Image();
        img.src = imageUrl;
        img.onload = () => {
            canvas.width = 256;
            canvas.height = 256;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, 256, 256);
            circles.forEach(circle => {
                ctx.beginPath();
                ctx.arc(circle.x, circle.y, circle.radius, 0, Math.PI * 2);
                ctx.fillStyle = circle.color;
                ctx.fill();
                ctx.strokeStyle = 'black';  // 设置边框颜色为黑色
                ctx.lineWidth = 0.5;  // 设置边框宽度
                ctx.stroke();  // 绘制边框
            });
        };
    }, [imageUrl, circles]);
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


    };
    return (
        <div className="flex flex-col items-center w-full min-h-screen p-5">
            <div className="grid w-full max-w-7xl gap-12 lg:grid-cols-3" style={{ height: 500 }}>
                <div className="p-6 bg-white rounded-3xl shadow-lg dark:bg-neutral-700">
                    <div className="text-center">
                        <h1 className="mb-8 text-2xl font-semibold text-neutral-600 lg:text-3xl">选择颜色:</h1>
                        <div className="flex justify-center space-x-2 mb-4">
                            {colors.map(({ color, label }) => (
                                <button
                                    key={color}
                                    className={`w-8 h-8 rounded-full ${selectedColor === color ? 'ring-2 ring-offset-2 ring-blue-500' : ''}`}
                                    style={{ backgroundColor: color }}
                                    title={label}
                                    onClick={() => handleColorClick(color)}
                                >
                                    <span className="sr-only">{label}</span>
                                </button>
                            ))}
                        </div>
                        <input
                            type="number"
                            value={radius} onChange={handleRadiusChange}
                            className="block w-full px-3 py-2 mb-4 border rounded-md dark:bg-transparent dark:border-white/10"
                            placeholder="半径"
                        />
                    </div>
                    <div className="overflow-y-auto max-h-60">
                        {circles.map((circle, index) => (
                            <div key={index} className="flex items-center justify-between p-2">
                                <span>房间: {circle.label} 半径: {circle.radius}</span>
                                <button className="text-red-500" onClick={() => removeCircle(index)}>删除</button>
                            </div>
                        ))}
                    </div>
                </div>
                <div className="p-6 bg-white rounded-3xl shadow-lg dark:bg-neutral-700">
                    <div className="flex items-center justify-center h-full">
                        <canvas ref={canvasRef} onClick={handleCanvasClick} />
                    </div>
                </div>
                <div className="p-6 bg-white rounded-3xl shadow-lg dark:bg-neutral-700">
    {generatedImageUrl && (
        <div className="flex flex-col items-center justify-center h-full">
            <img src={'http://localhost:8000/' + generatedImageUrl} alt="生成的图像" className="max-w-full max-h-full mb-4" />
            <button
                className="px-5 py-2 text-base font-medium text-white transition duration-500 ease-in-out transform bg-blue-600 rounded-xl lg:px-10 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                onClick={downloadImage}
            >
                下载图像
            </button>
        </div>
    )}
</div>
            </div>
            <div className="flex justify-center w-full mt-10 space-x-4">
                <button
                    className="px-5 py-4 text-base font-medium text-white transition duration-500 ease-in-out transform bg-blue-600 rounded-xl lg:px-10 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    onClick={() => fileInputRef.current.click()}
                >
                    选择图像
                </button>
                <input
                    type="file"
                    ref={fileInputRef} // 关联引用
                    style={{ display: 'none' }} // 隐藏文件输入框
                    onChange={handleImageChange}
                />
                <button
                    className="px-5 py-4 text-base font-medium text-white transition duration-500 ease-in-out transform bg-blue-600 rounded-xl lg:px-10 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    onClick={handleUpload}
                >
                    对抗生成模型
                </button>
                <button
                    className="px-5 py-4 text-base font-medium text-white transition duration-500 ease-in-out transform bg-blue-600 rounded-xl lg:px-10 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    onClick={handleUpload2}
                >
                    扩散模型
                </button>
            </div>
        </div>
    );
}

export default ImageUploader;

