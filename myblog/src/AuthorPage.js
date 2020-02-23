import React from 'react';
import { Layout } from 'antd';
import AdminHeader from './components/AdminHeader'
import AdminSideBar from './components/AdminSideBar';
import AuthorContent from './components/AuthorContent';

function AuthorPage() {
  return (
    <div>
      <Layout>
        <AdminHeader/>
        <Layout>
            <AdminSideBar defaultSelectedKeys="Authors"/>
            <Layout style={{ padding: '12px 24px 24px'}}><AuthorContent/></Layout>
        </Layout>
    </Layout>
    </div>
  );
}

export default AuthorPage;