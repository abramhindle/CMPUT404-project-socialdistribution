import React, {useState} from 'react'
import {Editor, EditorState} from 'draft-js'
interface richtextareaProps {
	id: string;
	name: string;
	placeholder?: string;
}

const RichTextArea: React.FC<richtextareaProps> = ({id, name, placeholder}) => {
	const [editorState, setEditorState] = useState(()=> EditorState.createEmpty())
		return (<div id={id}>
			<label htmlFor={id} className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{name}</label>
			<Editor placeholder={placeholder}  editorState={editorState} onChange={setEditorState}/>
		</div>);
}
export default RichTextArea