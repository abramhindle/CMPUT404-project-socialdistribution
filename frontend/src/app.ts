import { 
    provideFASTDesignSystem, 
  } from '@microsoft/fast-components';
import { FASTElement } from '@microsoft/fast-element';
import { appRegistry } from './appRegistry';

for (const component of appRegistry) {
    FASTElement.define(component.type, component.definition);
}
  
provideFASTDesignSystem()
      .register(
      ).withPrefix('');