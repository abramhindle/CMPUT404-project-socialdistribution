import { observable } from "@microsoft/fast-element";
import { PaginatedResponse } from "../libs/api-service/SocialApiModel";
import { Page } from "./Page";

export abstract class PaginatedPage extends Page {
    public loadMore?: HTMLElement;

    protected observer?: IntersectionObserver;

    @observable
    public paginatedResponse?: PaginatedResponse | null;

    constructor() {
        super();

        this.observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.getResults();
                }
            })
        })
    }

    protected abstract getResults(): any;
}