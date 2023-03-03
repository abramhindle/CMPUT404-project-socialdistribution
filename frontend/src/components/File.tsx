/* eslint-disable @next/next/no-img-element */
import React,{useState} from 'react'
import { FieldValues, UseFormRegister } from 'react-hook-form';
// From https://flowbite.com/docs/forms/file-input/
interface fileProps {
	id: string;
	filePreviewClass?: string;
	register: UseFormRegister<any>
	required?: boolean;
}

const File: React.FC<fileProps> = ({id, filePreviewClass, register, required}) => {
	const [file, setFile] = useState<File | null>(null);
	const [preview, setPreview] = useState<string | ArrayBuffer | null>(null);
	const [error, setError] = useState<string | null>(null);
	const hookRegister = register(id, {required: required})
		return (
			<div  className="">
		<div className="flex items-center justify-center w-full mb-4">
		<label htmlFor={id} className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
			<div className="flex flex-col items-center justify-center pt-5 pb-6">
				{!file && <svg aria-hidden="true" className="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>}
				{!file && <p className="mb-2 text-sm text-gray-500 dark:text-gray-400"><span className="font-semibold">Click to upload</span> or drag and drop</p>}
				{!file && <p className="text-xs text-gray-500 dark:text-gray-400">PNG or JPG(MAX. 800x400px)</p>}
				{file && <p className="text-xs text-gray-500 dark:text-gray-400 font-semibold">
					{file.name}
					</p>}
			</div>
			<input type="file" className="hidden" accept="image/png, image/jpeg"
				{...hookRegister}
				id={id}
				onChange={(e) => {
					hookRegister.onChange(e);
					setFile(e.target.files?.[0] ?? null);
					setError(null);
					if (e.target.files?.[0]) {
						const reader = new FileReader();
						reader.onloadend = () => {
							setPreview(reader.result);
						};
						reader.readAsDataURL(e.target.files[0]);

						
					}

				}}

				
			/>
			
		</label>
	</div>
			<div className={`flex flex-col  w-fit h-full mb-6 bg-gray-50 p-7 rounded-xl shadow-sm border border-gray-100 ${file ? '' : 'hidden'}`}>
							<span className="block mb-5 text-sm font-medium text-gray-900 dark:text-white">Preview</span>
							{error && <p className="text-xs text-red-500">{error}</p>}
							{preview && <img src={preview as string} className={filePreviewClass} alt='Preview'/>}
				</div>
					
				</div> );
}
export default File