'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';

function DashboardContent() {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800">대시보드</h1>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
            >
              로그아웃
            </button>
          </div>

          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl p-6 text-white mb-8">
            <h2 className="text-xl font-semibold mb-2">
              환영합니다, {user?.username}님!
            </h2>
            <p className="opacity-90">
              로그인에 성공했습니다. 이제 모든 기능을 사용할 수 있습니다.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-gray-50 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                계정 정보
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">사용자 이름</span>
                  <span className="font-medium text-gray-800">
                    {user?.username}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">이메일</span>
                  <span className="font-medium text-gray-800">{user?.email}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">계정 상태</span>
                  <span
                    className={`font-medium ${
                      user?.is_active ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    {user?.is_active ? '활성' : '비활성'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">가입일</span>
                  <span className="font-medium text-gray-800">
                    {user?.created_at ? formatDate(user.created_at) : '-'}
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-gray-50 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                빠른 링크
              </h3>
              <div className="space-y-3">
                <a
                  href="/"
                  className="block w-full bg-white border border-gray-200 rounded-lg px-4 py-3 text-gray-700 hover:bg-indigo-50 hover:border-indigo-200 transition-colors"
                >
                  홈으로 이동
                </a>
                <button
                  onClick={handleLogout}
                  className="block w-full bg-white border border-gray-200 rounded-lg px-4 py-3 text-gray-700 hover:bg-red-50 hover:border-red-200 transition-colors text-left"
                >
                  로그아웃
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
}
