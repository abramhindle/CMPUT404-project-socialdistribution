import React from 'react';
import { Layout } from 'antd';
import AdminHeader from './components/AdminHeader'
import AdminSideBar from './components/AdminSideBar';
import SignUpRequestContent from './components/SignUpRequestContent';

function SignUpRequestPage() {
  return (
    <div>
      <Layout>
        <AdminHeader></AdminHeader>
        <Layout>
            <AdminSideBar defaultSelectedKeys="SignUpRequest"></AdminSideBar>
            <Layout style={{ padding: '12px 24px 24px'}}><SignUpRequestContent /></Layout>
        </Layout>
    </Layout>
    </div>
  );
}

export default SignUpRequestPage;