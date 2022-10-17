import { 
    provideFASTDesignSystem, 
  } from '@microsoft/fast-components';
import { appRegistry } from './appRegistry';

appRegistry;
  
provideFASTDesignSystem()
      .register(
            // Register components here
      ).withPrefix('');