import { FASTElement, PartialFASTElementDefinition } from "@microsoft/fast-element";

export class ComponentEntry {
    public definition: PartialFASTElementDefinition;
    public type: any;

    constructor(definition: PartialFASTElementDefinition, type: any) {
        this.definition = definition;
        this.type = type;
    }
}

export const defineComponent = (component: ComponentEntry) => {
    FASTElement.define(component.type, component.definition);
}
