export interface ModalUnstyledClasses {
    /** Class name applied to the root element. */
    root: string;
    /** Class name applied to the root element if the `Modal` has exited. */
    hidden: string;
    /** Class name applied to the backdrop element. */
    backdrop: string;
}
export type ModalUnstyledClassKey = keyof ModalUnstyledClasses;
export declare function getModalUtilityClass(slot: string): string;
declare const modalUnstyledClasses: ModalUnstyledClasses;
export default modalUnstyledClasses;
