import { Page } from "../Page";
import {attr} from "@microsoft/fast-element";

export class ViewPost extends Page {

  @attr post_text: string = 'Example Post Text';
  @attr post_author: string = 'Zebra Zigby';
  @attr post_edit_date: string = '2022-10-13';
  @attr post_image_url: string = 'https://play.teleporthq.io/static/svg/default-img.svg';
  @attr comments: {display_name: string, content: string}[] = [
    {display_name: 'Test Name', content: 'Comment content'}
  ]

  public connectedCallback() {
    super.connectedCallback();
  }
}
