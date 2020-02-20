import React from 'react';
// import './AdminMainPage.css';
import { Layout } from 'antd';
import AdminHeader from './components/AdminHeader'
import AdminSideBar from './components/AdminSideBar';
import AdminContent from './components/AdminContent';

function AdminMainPage() {
  return (
    <div>
      <Layout>
        <AdminHeader></AdminHeader>
        <Layout>
          <AdminSideBar></AdminSideBar>
          <Layout style={{ padding: '12px 24px 24px'}}><AdminContent /></Layout>
          {/* <Layout style={{padding: '12px 24px 24px'}}><TestContent /></Layout> */}
        </Layout>
    </Layout>
    </div>
  );
}

export default AdminMainPage;