import { css } from "@microsoft/fast-element";
import { ResetStyles } from "./reset.styles";
import { DefaultStyles } from "./default.styles";
import { GeneralStyles } from "./general.styles";
import { accentFillRest, accentForegroundActive, accentForegroundRest, neutralLayer2, neutralLayer4, typeRampPlus1FontSize, typeRampPlus2FontSize } from "@microsoft/fast-components";

export const ViewPostPageStyles = css`
	${ResetStyles}
	${DefaultStyles}
	${GeneralStyles}
	
	.post-container {
		width: 100%;
		display: flex;
		overflow: auto;
		min-height: 100vh;
		align-items: center;
		flex-direction: column;
	}

	.post-container1 {
		flex: 0 0 auto;
		width: 90%;
		display: flex;
		margin-top: var(--dl-space-space-twounits);
		align-items: center;
		padding-top: var(--dl-space-space-halfunit);
		padding-left: var(--dl-space-space-halfunit);
		border-radius: var(--dl-radius-radius-radius4);
		padding-right: var(--dl-space-space-halfunit);
		padding-bottom: var(--dl-space-space-halfunit);
		margin-bottom: 8px;
		justify-content: flex-start;
		background-color: white;
		border-top-left-radius: var(--dl-radius-radius-radius4);
		border-top-right-radius: var(--dl-radius-radius-radius4);
		border-bottom-left-radius: var(--dl-radius-radius-radius4);
		border-bottom-right-radius: var(--dl-radius-radius-radius4);
	}

	.post-image {
		flex: 1 1 0;
		max-width: 100px;
		object-fit: cover;
		margin-right: var(--dl-space-space-unit);
		border-radius: var(--dl-radius-radius-radius4);
		border-top-left-radius: var(--dl-radius-radius-radius4);
		border-top-right-radius: var(--dl-radius-radius-radius4);
		border-bottom-left-radius: var(--dl-radius-radius-radius4);
		border-bottom-right-radius: var(--dl-radius-radius-radius4);
	}

	.post-container2 {
		flex: 3 1 0;
		display: flex;
		position: relative;
		align-items: flex-start;
		flex-direction: column;
		justify-content: flex-start;
		width: 100%;
	}

	.post-text {
		margin-top: var(--dl-space-space-halfunit);
	}

	.post-container3 {
		flex: 0 0 auto;
		right: 0px;
		width: 100%;
		bottom: 0px;
		height: 30%;
	}
	
	.post-action-icon {
		width: 25px;
		height: 25px;
		cursor: pointer;
	}

	.liked {
		color: #14A9FF;
	}

	.post-action-icon:hover {
		color: ${accentForegroundActive};
	}

	.see-likes {
		cursor: pointer;
	}

	fast-dialog {
		z-index: 5;
	}

	.see-likes:hover {
		text-decoration: underline;
	}

	.post-ul {
		width: 80%;
		height: 80%;
		overflow: auto;
		align-self: center;
		padding-left: 0px;
		border-radius: var(--dl-radius-radius-radius4);
		border-top-left-radius: var(--dl-radius-radius-radius4);
		border-top-right-radius: var(--dl-radius-radius-radius4);
		border-bottom-left-radius: var(--dl-radius-radius-radius4);
		border-bottom-right-radius: var(--dl-radius-radius-radius4);
	}

	.post-li {
		border-radius: var(--dl-radius-radius-radius4);
		border-top-left-radius: var(--dl-radius-radius-radius4);
		border-top-right-radius: var(--dl-radius-radius-radius4);
		border-bottom-left-radius: var(--dl-radius-radius-radius4);
		border-bottom-right-radius: var(--dl-radius-radius-radius4);
	}

	.comment-container {
		display: flex;
		flex-direction: column;
		padding: 8px;
		border-radius: 16px;
		background-color: ${neutralLayer4};
		margin: 8px;
	}

	.comments-box {
		width: 90%
	}

	.comment-display-name {
		margin-top: var(--dl-space-space-halfunit);
		margin-left: var(--dl-space-space-unit);
		border-radius: var(--dl-radius-radius-radius4);
		margin-bottom: var(--dl-space-space-halfunit);
		border-top-left-radius: var(--dl-radius-radius-radius4);
		border-top-right-radius: var(--dl-radius-radius-radius4);
		border-bottom-left-radius: var(--dl-radius-radius-radius4);
		border-bottom-right-radius: var(--dl-radius-radius-radius4);
	}

	.comment-content {
		overflow: hidden;
	}

	.comment-profile-icon {
		top: 0px;
		right: 0px;
		width: auto;
		height: 100%;
		position: absolute;
		object-fit: cover;
		border-radius: var(--dl-radius-radius-radius4);
		border-top-left-radius: var(--dl-radius-radius-radius4);
		border-top-right-radius: var(--dl-radius-radius-radius4);
		border-bottom-left-radius: var(--dl-radius-radius-radius4);
		border-bottom-right-radius: var(--dl-radius-radius-radius4);
	}

	.post-information {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.post-actions {
		display: flex;
		justify-content: space-around;
		align-items: center;
	}

	#likes-modal, #comments-modal {
        position: fixed;
        z-index: 5;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto; 
        background-color: rgba(0, 0, 0, 0.4);
    }

    .modal-content {
        background-color: white;
        margin: 15% auto;
        padding: 20px;
        border-radius: 20px;
        width: 70%;
		background: linear-gradient(to bottom right, ${neutralLayer2}, ${accentFillRest});
    }

	.modal-content ul {
		max-height: 60vh;
    	overflow: auto;
	}

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: ${typeRampPlus2FontSize};
        font-weight: bold;
    }

    .modal-header button, .make-comment {
        border-radius: 50px;
        padding: 8px 20px;
        border: 0;
        background-color: black;
        color: white;
        font-size: ${typeRampPlus1FontSize};
        cursor: pointer;
    }

	.make-comment {
		background-color: ${accentForegroundRest};
		font-size: ${typeRampPlus2FontSize};
	}

	.modal-open {
        display: block;
    }

    .modal-close {
        display: none;
    }

	.post-comment-area {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
	}

	.post-comment-area textarea {
		width: 100%;
		height: 30vh;
		resize: none;
		margin: 16px 0;
	}

	.edit-post-button {
		border-radius: 50px;
		font-size: ${typeRampPlus1FontSize};
		padding: 0 16px;
		height: 5vh;
		font-weight: bold;

		display: flex;
		place-content: center;
		align-items: center;
		cursor: pointer;

		background-color: white;
		border: 2px solid lightgrey;
		color: black;

		width: 90%;
	}

	.margin-bottom {
		margin-bottom: 5rem;
	}

	@media (max-width: 991px) {
		.post-container4 {
		position: relative;
		}

		.post-image1 {
		top: 0px;
		right: 0px;
		width: auto;
		height: 100%;
		position: absolute;
		}

		.post-container5 {
		position: relative;
		}

		.post-image2 {
		top: 0px;
		right: 0px;
		width: auto;
		height: 100%;
		position: absolute;
		}

		.post-container6 {
		position: relative;
		}

		.post-image3 {
		top: 0px;
		right: 0px;
		width: auto;
		height: 100%;
		position: absolute;
		}
	}
`;
