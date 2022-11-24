import { library } from "@fortawesome/fontawesome-svg-core";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { FASTElement, observable } from "@microsoft/fast-element";
import { SocialApi } from "../../libs/api-service/SocialApi";
import { Author } from "../../libs/api-service/SocialApiModel";
import { SocialApiTransform } from "../../libs/api-service/SocialApiTransform";
import { LayoutType } from "../../libs/core/PageModel";

const MAX_RESULTS = 10;

export class SocialSearch extends FASTElement {
    @observable
    public userId?: string;

    @observable
    public user?: Author | null;

    @observable
    public layoutType: LayoutType = LayoutType.Desktop;

    @observable
    public layoutStyleClass: string = "";

    @observable
    public searchInput?: HTMLInputElement;

    @observable
    public searchResults: any[] = [];

    private authors: Author[] = [];

    constructor() {
        super()
        this.addIcons();
        this.getAuthors();
    }

    public connectedCallback() {
        super.connectedCallback();
        const searchResults = this.searchResults
        const userId = this.userId
        if (this.searchInput) {
            this.searchInput.addEventListener('input', (ev) => {
                if (!this.searchInput) {
                    return;
                }

                // Clear results
                this.searchResults.splice(0, this.searchResults.length);

                let input = this.searchInput?.value
                if (this.searchInput && input?.trim().toLowerCase()?.length > 0) {
                    // Trim input
                    input = input?.trim().toLowerCase()
                    
                    let taken = 0
                    let index = 0
                    while (index < this.authors.length && taken < MAX_RESULTS) {
                        console.log(this.authors[index].displayName, input)
                        if (this.authors[index].displayName.includes(input) && this.authors[index].id != userId) {
                            searchResults.push(this.authors[index])
                            taken += 1
                        }
                        index += 1
                    }
                    console.log(searchResults)
                }
            })
        }
    }

    private addIcons() {
        library.add(faSearch);
    }

    private async getAuthors() {
        try {
            const responseData = await SocialApi.fetchAuthors();
            if (responseData) {
                this.parseProfiles(responseData)
            }
        } catch (e) {
            console.error("Author fetch failed", e);
        }
    }

    private parseProfiles(profiles: any[]) {
        if (!profiles) {
            return;
        }

        for (const authorData of profiles) {
            if (!authorData.type || authorData.type == "author") {
                const author = SocialApiTransform.authorDataTransform(authorData);
                if (author) {
                    author.displayName = author.displayName.toLowerCase()
                    this.authors.push(author);
                }
            }
        }

        console.log(this.authors)
    }
}