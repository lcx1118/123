// FeatureTwo.js (假设在pages/auth/目录下)
// import React, { useState } from 'react';
// import Link from 'next/link';
//
// function FeatureTwo() {
//     const [file, setFile] = useState(null);
//
//     const handleFileChange = (event) => {
//         setFile(event.target.files[0]);
//     };
//
//     const handleUpload = async () => {
//         const formData = new FormData();
//         formData.append('cadfile', file);
//
//         const response = await fetch('http://localhost:8000/api/upload-boundary/', {
//             method: 'POST',
//             body: formData,
//         });
//         const data = await response.json();
//
//         alert(data.message); // 显示来自后端的消息
//     };
//
//     return (
//         <div>
//             <h1>上传或绘制边界框</h1>
//             <input type="file" onChange={handleFileChange} />
//             <button onClick={handleUpload}>上传边界框</button>
//             <Link href="/auth/FeatureThree">下一步</Link>
//         </div>
//     );
// }
//
// export default FeatureTwo;
import React, { useState } from 'react';
import Link from 'next/link';

function FeatureTwo() {

    const [file, setFile] = useState(null);
    const [imageUrl, setImageUrl] = useState('');

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('cadfile', file);

        const response = await fetch('http://localhost:8000/api/upload-boundary/', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        // console.log(data);
        alert(data.message);  // 显示来自后端的消息
        if (response.ok) {
            // console.log("11111111")
            const fullImageUrl = `http://localhost:8000${data.imageUrl}`;  // 确保使用完整的 URL

            setImageUrl(fullImageUrl);  // 保存图片 URL
        }
    };
    // console.log(imageUrl)
    return (
        <div>
            <h1>上传或绘制边界框</h1>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>上传边界框</button>

            {imageUrl && (
                <Link href={`/auth/FeatureThree?imageUrl=${imageUrl}`}>下一步</Link>)}
        </div>
    );
}

//    {imageUrl && <img src={imageUrl} alt="Converted CAD" />}
export default FeatureTwo;
