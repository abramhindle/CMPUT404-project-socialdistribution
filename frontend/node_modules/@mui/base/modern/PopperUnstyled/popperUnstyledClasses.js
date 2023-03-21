import generateUtilityClass from '../generateUtilityClass';
import generateUtilityClasses from '../generateUtilityClasses';
export function getPopperUnstyledUtilityClass(slot) {
  return generateUtilityClass('MuiPopper', slot);
}
const popperUnstyledClasses = generateUtilityClasses('MuiPopper', ['root']);
export default popperUnstyledClasses;