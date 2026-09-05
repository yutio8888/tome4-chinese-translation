import {checkManifest} from './build-manifest.mjs';
import {checkFreeze} from './freezer.mjs';

// Runtime authority is the complete static manifest plus the reproducible request freeze.
// Any static file addition/removal/change, including either integrity builder itself, fails.
export function runtimeChecks(root){
 const errors=checkManifest(root).map(x=>`RUNTIME_${x}`),freeze=checkFreeze(root);
 errors.push(...freeze.errors.map(x=>`RUNTIME_FREEZE:${x}`));
 return errors;
}
