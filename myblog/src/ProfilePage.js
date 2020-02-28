import React from 'react';
import { Layout } from 'antd';
import AdminHeader from './components/AdminHeader'
import AdminSideBar from './components/AdminSideBar';
import ProfileContent from './components/ProfileContent';

function ProfilePage() {
  return (
    <div>
        <Layout>
            <AdminHeader></AdminHeader>
            <Layout>
                <AdminSideBar defaultSelectedKeys="None"></AdminSideBar>
                <Layout><ProfileContent /></Layout>
            </Layout>
        </Layout>
    </div>
  );
}

export default ProfilePage;