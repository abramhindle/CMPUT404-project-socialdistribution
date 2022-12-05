import { FollowStatus, LayoutStyleClass, LayoutType } from "./PageModel";

export namespace LayoutHelpers {
    export function getLayoutStyle(layoutType: LayoutType) {
        switch (layoutType) {
            case LayoutType.Desktop:
                return LayoutStyleClass.Desktop
            case LayoutType.Tablet:
                return LayoutStyleClass.Tablet
            default:
                return LayoutStyleClass.Mobile
        }
    }

    export function parseFollowStatus(followStatus: FollowStatus): string {
        switch (followStatus) {
            case FollowStatus.Following:
                return "Following";
            case FollowStatus.NotFollowing:
                return "Follow";
            case FollowStatus.Sent:
                return "Sent";
            default:
                return "";
        }
    }
}

export namespace ImageHelpers {
    export function convertBase64(file: any): Promise<string | ArrayBuffer | null> {
        return new Promise((resolve, reject) => {
            const fileReader = new FileReader();
            fileReader.readAsDataURL(file);

            fileReader.onload = () => {
                resolve(fileReader.result);
            };

            fileReader.onerror = (error) => {
                reject(error);
            };
        });
    }
}