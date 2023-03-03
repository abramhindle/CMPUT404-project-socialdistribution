// From https://flowbite.com/docs/forms/input-field/
import { FieldValues, UseFormRegister } from 'react-hook-form';

interface inputProps {
	id: string;
	name: string;
	placeholder?: string;
	required?: boolean;
	extraClass?: string;
	register: UseFormRegister<any>;
}

const Input: React.FC<inputProps> = ({id, name, placeholder, required, extraClass, register}) => {
		return (<div className={`${extraClass}`}>
		<label htmlFor={id} className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{name}</label>
		<input type="text" 
			{...register(id, {required: required})}
		 className="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light" placeholder={placeholder} />
		 </div>);
}
export default Input;