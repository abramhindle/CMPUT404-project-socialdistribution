import * as NodeNotifier from 'node-notifier';
export interface Notification extends NodeNotifier.Notification {
    force?: boolean;
}
export declare function notify(notification?: Notification, callback?: NodeNotifier.NotificationCallback): NodeNotifier.NodeNotifier | undefined;
