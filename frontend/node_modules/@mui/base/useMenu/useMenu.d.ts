import { MenuItemMetadata, UseMenuListboxSlotProps, UseMenuParameters } from './useMenu.types';
import { EventHandlers } from '../utils';
import { type MenuUnstyledContextType } from '../MenuUnstyled';
/**
 *
 * Demos:
 *
 * - [Unstyled Menu](https://mui.com/base/react-menu/#hooks)
 *
 * API:
 *
 * - [useMenu API](https://mui.com/base/api/use-menu/)
 */
export default function useMenu(parameters?: UseMenuParameters): {
    contextValue: MenuUnstyledContextType;
    getListboxProps: <TOther extends EventHandlers>(otherHandlers?: TOther) => UseMenuListboxSlotProps;
    highlightedOption: string | null;
    highlightFirstItem: () => void;
    highlightLastItem: () => void;
    menuItems: Record<string, MenuItemMetadata>;
};
