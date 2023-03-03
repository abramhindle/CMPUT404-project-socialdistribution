import React from 'react'

interface selectProps {
	options: {name: string, value: string}[];
	name: string;
	id: string;
	value?: string;
	setValue?: (value: string) => void;
}

const select: React.FC<selectProps> = ({name, id, options, value, setValue}) => {
		return (<div className='mb-4'><label htmlFor={id} className="sr-only">{name}</label>
		<select value={value} onChange={
			(e) => {
				if (setValue) {
					setValue(e.target.value);
				}
			}
		} id={id} className="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-200 appearance-none dark:text-gray-400 dark:border-gray-700 focus:outline-none focus:ring-0 focus:border-gray-200 peer">
		{options.map((option) => {
			return (<option key={option.value} value={option.value}>{option.name}</option>);
		})}
		</select></div>);
}
export default select