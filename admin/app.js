// API 基础路径
const API_BASE = '/api/v1';

// 管理员 Token
let adminToken = localStorage.getItem('adminToken') || '';

// 状态映射
const ORDER_STATUS = { 0: '待付款', 1: '待发货', 2: '待收货', 3: '已完成', 4: '已取消' };
const ORDER_STATUS_COLOR = { 0: 'yellow', 1: 'blue', 2: 'purple', 3: 'green', 4: 'gray' };

// 当前页面
let currentPage = 'dashboard';
let currentOrderStatus = '';
let categories = [];

// 检查登录状态
function checkAuth() {
  if (adminToken) {
    document.getElementById('loginPage').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    const adminInfo = JSON.parse(localStorage.getItem('adminInfo') || '{}');
    document.getElementById('adminName').textContent = adminInfo.username || '管理员';
    showPage('dashboard');
  } else {
    document.getElementById('loginPage').classList.remove('hidden');
    document.getElementById('app').classList.add('hidden');
  }
}

// 登录表单
document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('loginUsername').value;
  const password = document.getElementById('loginPassword').value;
  const errorEl = document.getElementById('loginError');
  
  try {
    const res = await fetch(API_BASE + '/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    
    if (data.code === 200) {
      adminToken = data.data.token;
      localStorage.setItem('adminToken', adminToken);
      localStorage.setItem('adminInfo', JSON.stringify({ username: data.data.username }));
      errorEl.classList.add('hidden');
      checkAuth();
    } else {
      errorEl.textContent = data.message || '登录失败';
      errorEl.classList.remove('hidden');
    }
  } catch (err) {
    errorEl.textContent = '网络错误';
    errorEl.classList.remove('hidden');
  }
});

// 页面切换
function showPage(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
  document.getElementById(`page-${page}`).classList.remove('hidden');
  
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('bg-gray-700'));
  document.querySelector(`.nav-item[data-page="${page}"]`).classList.add('bg-gray-700');
  
  const titles = {
    dashboard: '仪表盘', products: '商品管理', categories: '分类管理',
    orders: '订单管理', users: '用户管理', coupons: '优惠券管理', banners: '轮播图管理'
  };
  document.getElementById('pageTitle').textContent = titles[page];
  currentPage = page;
  
  // 加载数据
  if (page === 'dashboard') loadDashboard();
  else if (page === 'products') loadProducts();
  else if (page === 'categories') loadCategories();
  else if (page === 'orders') loadOrders();
  else if (page === 'users') loadUsers();
  else if (page === 'coupons') loadCoupons();
  else if (page === 'banners') loadBanners();
}

// API 请求
async function api(url, options = {}) {
  const res = await fetch(API_BASE + url, {
    ...options,
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${adminToken}`,
      ...options.headers 
    }
  });
  const data = await res.json();
  if (data.code === 401) {
    // Token 过期，退出登录
    logout();
    return { data: null };
  }
  return data;
}

// 仪表盘
async function loadDashboard() {
  const [products, orders, users] = await Promise.all([
    api('/admin/stats/products'),
    api('/admin/stats/orders'),
    api('/admin/stats/users')
  ]);
  
  document.getElementById('stat-products').textContent = products.data?.count || 0;
  document.getElementById('stat-orders').textContent = orders.data?.count || 0;
  document.getElementById('stat-users').textContent = users.data?.count || 0;
  document.getElementById('stat-sales').textContent = '¥' + (orders.data?.total_amount || 0);
  
  // 最近订单
  const recent = await api('/admin/orders?page=1&size=5');
  const tbody = document.getElementById('recent-orders');
  tbody.innerHTML = (recent.data?.items || []).map(o => `
    <tr class="border-t">
      <td class="px-4 py-3 text-sm">${o.order_no}</td>
      <td class="px-4 py-3 text-sm">${o.user?.username || '-'}</td>
      <td class="px-4 py-3 text-sm text-red-500 font-medium">¥${o.total_amount}</td>
      <td class="px-4 py-3"><span class="px-2 py-1 text-xs rounded bg-${ORDER_STATUS_COLOR[o.status]}-100 text-${ORDER_STATUS_COLOR[o.status]}-600">${ORDER_STATUS[o.status]}</span></td>
      <td class="px-4 py-3 text-sm text-gray-500">${formatTime(o.created_at)}</td>
    </tr>
  `).join('');
}

// 商品管理
async function loadProducts() {
  const [res, cats] = await Promise.all([
    api('/admin/products'),
    api('/categories')
  ]);
  categories = cats.data || [];
  
  const tbody = document.getElementById('products-list');
  tbody.innerHTML = (res.data || []).map(p => `
    <tr class="border-t">
      <td class="px-4 py-3 text-sm">${p.id}</td>
      <td class="px-4 py-3"><img src="${p.cover}" class="w-12 h-12 object-cover rounded"></td>
      <td class="px-4 py-3 text-sm">${p.name}</td>
      <td class="px-4 py-3 text-sm">${getCategoryName(p.category_id)}</td>
      <td class="px-4 py-3 text-sm text-red-500">¥${p.base_price}</td>
      <td class="px-4 py-3 text-sm">${p.sales}</td>
      <td class="px-4 py-3"><span class="px-2 py-1 text-xs rounded ${p.status ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'}">${p.status ? '上架' : '下架'}</span></td>
      <td class="px-4 py-3 text-sm space-x-2">
        <button onclick="editProduct(${p.id})" class="text-blue-500 hover:text-blue-700"><i class="ri-edit-line"></i></button>
        <button onclick="deleteProduct(${p.id})" class="text-red-500 hover:text-red-700"><i class="ri-delete-bin-line"></i></button>
      </td>
    </tr>
  `).join('');
}

function getCategoryName(id) {
  const cat = categories.find(c => c.id === id);
  return cat ? cat.name : '-';
}

function showProductModal(product = null) {
  document.getElementById('productModalTitle').textContent = product ? '编辑商品' : '添加商品';
  document.getElementById('productId').value = product?.id || '';
  document.getElementById('productName').value = product?.name || '';
  document.getElementById('productCover').value = product?.cover || '';
  document.getElementById('productImages').value = (product?.images || []).join('\n');
  document.getElementById('productDesc').value = product?.description || '';
  document.getElementById('productPrice').value = product?.base_price || '';
  document.getElementById('productStatus').value = product?.status ?? 1;
  
  // 填充分类下拉
  const select = document.getElementById('productCategory');
  select.innerHTML = categories.map(c => `<option value="${c.id}" ${product?.category_id === c.id ? 'selected' : ''}>${c.name}</option>`).join('');
  
  document.getElementById('productModal').classList.add('show');
}

async function editProduct(id) {
  const res = await api(`/products/${id}`);
  if (res.data) showProductModal(res.data);
}

async function deleteProduct(id) {
  if (!confirm('确定删除该商品？')) return;
  await api(`/admin/products/${id}`, { method: 'DELETE' });
  loadProducts();
}

// 分类管理
async function loadCategories() {
  const res = await api('/categories');
  categories = res.data || [];
  
  const tbody = document.getElementById('categories-list');
  tbody.innerHTML = categories.map(c => `
    <tr class="border-t">
      <td class="px-4 py-3 text-sm">${c.id}</td>
      <td class="px-4 py-3"><img src="${c.icon || '/static/logo.png'}" class="w-10 h-10 object-cover rounded"></td>
      <td class="px-4 py-3 text-sm">${c.name}</td>
      <td class="px-4 py-3 text-sm">${c.sort_order}</td>
      <td class="px-4 py-3 text-sm space-x-2">
        <button onclick="editCategory(${c.id})" class="text-blue-500 hover:text-blue-700"><i class="ri-edit-line"></i></button>
        <button onclick="deleteCategory(${c.id})" class="text-red-500 hover:text-red-700"><i class="ri-delete-bin-line"></i></button>
      </td>
    </tr>
  `).join('');
}

function showCategoryModal(category = null) {
  document.getElementById('categoryModalTitle').textContent = category ? '编辑分类' : '添加分类';
  document.getElementById('categoryId').value = category?.id || '';
  document.getElementById('categoryName').value = category?.name || '';
  document.getElementById('categoryIcon').value = category?.icon || '';
  document.getElementById('categorySortOrder').value = category?.sort_order || 0;
  document.getElementById('categoryModal').classList.add('show');
}

function editCategory(id) {
  const cat = categories.find(c => c.id === id);
  if (cat) showCategoryModal(cat);
}

async function deleteCategory(id) {
  if (!confirm('确定删除该分类？')) return;
  await api(`/admin/categories/${id}`, { method: 'DELETE' });
  loadCategories();
}

// 订单管理
async function loadOrders(status = '') {
  const url = status !== '' ? `/admin/orders?status=${status}` : '/admin/orders';
  const res = await api(url);
  
  const tbody = document.getElementById('orders-list');
  tbody.innerHTML = (res.data?.items || res.data || []).map(o => `
    <tr class="border-t">
      <td class="px-4 py-3 text-sm">${o.order_no}</td>
      <td class="px-4 py-3 text-sm">${o.user?.username || '-'}</td>
      <td class="px-4 py-3 text-sm">${o.items?.length || 0}件商品</td>
      <td class="px-4 py-3 text-sm text-red-500 font-medium">¥${o.total_amount}</td>
      <td class="px-4 py-3"><span class="px-2 py-1 text-xs rounded bg-${ORDER_STATUS_COLOR[o.status]}-100 text-${ORDER_STATUS_COLOR[o.status]}-600">${ORDER_STATUS[o.status]}</span></td>
      <td class="px-4 py-3 text-sm text-gray-500">${formatTime(o.created_at)}</td>
      <td class="px-4 py-3 text-sm space-x-2">
        ${o.status === 1 ? `<button onclick="shipOrder(${o.id})" class="text-blue-500 hover:text-blue-700">发货</button>` : ''}
      </td>
    </tr>
  `).join('');
}

function filterOrders(status) {
  currentOrderStatus = status;
  document.querySelectorAll('.order-tab').forEach(t => t.classList.remove('tab-active'));
  event.target.classList.add('tab-active');
  loadOrders(status);
}

async function shipOrder(id) {
  if (!confirm('确定发货？')) return;
  await api(`/admin/orders/${id}/ship`, { method: 'PUT' });
  loadOrders(currentOrderStatus);
}

// 用户管理
async function loadUsers() {
  const res = await api('/admin/users');
  
  const tbody = document.getElementById('users-list');
  tbody.innerHTML = (res.data || []).map(u => `
    <tr class="border-t">
      <td class="px-4 py-3 text-sm">${u.id}</td>
      <td class="px-4 py-3 text-sm">${u.username}</td>
      <td class="px-4 py-3 text-sm">${u.phone || '-'}</td>
      <td class="px-4 py-3 text-sm text-gray-500">${formatTime(u.created_at)}</td>
      <td class="px-4 py-3"><span class="px-2 py-1 text-xs rounded bg-green-100 text-green-600">正常</span></td>
    </tr>
  `).join('');
}

// 优惠券管理
async function loadCoupons() {
  const res = await api('/admin/coupons');
  
  const tbody = document.getElementById('coupons-list');
  tbody.innerHTML = (res.data || []).map(c => `
    <tr class="border-t">
      <td class="px-4 py-3 text-sm">${c.id}</td>
      <td class="px-4 py-3 text-sm">${c.name}</td>
      <td class="px-4 py-3 text-sm">${c.type === 1 ? '满减券' : '折扣券'}</td>
      <td class="px-4 py-3 text-sm text-red-500">${c.type === 1 ? '¥' + c.value : c.value * 10 + '折'}</td>
      <td class="px-4 py-3 text-sm">满¥${c.min_amount}</td>
      <td class="px-4 py-3 text-sm">${c.remain}/${c.total}</td>
      <td class="px-4 py-3 text-sm text-gray-500">${formatDate(c.end_time)}</td>
      <td class="px-4 py-3 text-sm">
        <button onclick="deleteCoupon(${c.id})" class="text-red-500 hover:text-red-700"><i class="ri-delete-bin-line"></i></button>
      </td>
    </tr>
  `).join('');
}

function showCouponModal() {
  document.getElementById('couponForm').reset();
  document.getElementById('couponId').value = '';
  document.getElementById('couponModal').classList.add('show');
}

async function deleteCoupon(id) {
  if (!confirm('确定删除该优惠券？')) return;
  await api(`/admin/coupons/${id}`, { method: 'DELETE' });
  loadCoupons();
}

// 轮播图管理
async function loadBanners() {
  const res = await api('/banners');
  
  const tbody = document.getElementById('banners-list');
  tbody.innerHTML = (res.data || []).map(b => `
    <tr class="border-t">
      <td class="px-4 py-3 text-sm">${b.id}</td>
      <td class="px-4 py-3"><img src="${b.image}" class="w-24 h-12 object-cover rounded"></td>
      <td class="px-4 py-3 text-sm">${b.link || '-'}</td>
      <td class="px-4 py-3 text-sm">${b.sort_order}</td>
      <td class="px-4 py-3 text-sm space-x-2">
        <button onclick="editBanner(${b.id})" class="text-blue-500 hover:text-blue-700"><i class="ri-edit-line"></i></button>
        <button onclick="deleteBanner(${b.id})" class="text-red-500 hover:text-red-700"><i class="ri-delete-bin-line"></i></button>
      </td>
    </tr>
  `).join('');
}

let bannersData = [];
function showBannerModal(banner = null) {
  document.getElementById('bannerModalTitle').textContent = banner ? '编辑轮播图' : '添加轮播图';
  document.getElementById('bannerId').value = banner?.id || '';
  document.getElementById('bannerImage').value = banner?.image || '';
  document.getElementById('bannerLink').value = banner?.link || '';
  document.getElementById('bannerSortOrder').value = banner?.sort_order || 0;
  document.getElementById('bannerModal').classList.add('show');
}

async function editBanner(id) {
  const res = await api('/banners');
  const banner = (res.data || []).find(b => b.id === id);
  if (banner) showBannerModal(banner);
}

async function deleteBanner(id) {
  if (!confirm('确定删除该轮播图？')) return;
  await api(`/admin/banners/${id}`, { method: 'DELETE' });
  loadBanners();
}

// 弹窗控制
function closeModal(id) {
  document.getElementById(id).classList.remove('show');
}

// 表单提交
document.getElementById('productForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('productId').value;
  const data = {
    name: document.getElementById('productName').value,
    category_id: parseInt(document.getElementById('productCategory').value),
    cover: document.getElementById('productCover').value,
    images: document.getElementById('productImages').value.split('\n').filter(s => s.trim()),
    description: document.getElementById('productDesc').value,
    base_price: parseFloat(document.getElementById('productPrice').value),
    status: parseInt(document.getElementById('productStatus').value)
  };
  
  if (id) {
    await api(`/admin/products/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  } else {
    await api('/admin/products', { method: 'POST', body: JSON.stringify(data) });
  }
  closeModal('productModal');
  loadProducts();
});

document.getElementById('categoryForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('categoryId').value;
  const data = {
    name: document.getElementById('categoryName').value,
    icon: document.getElementById('categoryIcon').value,
    sort_order: parseInt(document.getElementById('categorySortOrder').value)
  };
  
  if (id) {
    await api(`/admin/categories/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  } else {
    await api('/admin/categories', { method: 'POST', body: JSON.stringify(data) });
  }
  closeModal('categoryModal');
  loadCategories();
});

document.getElementById('couponForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    name: document.getElementById('couponName').value,
    type: parseInt(document.getElementById('couponType').value),
    value: parseFloat(document.getElementById('couponValue').value),
    min_amount: parseFloat(document.getElementById('couponMinAmount').value),
    total: parseInt(document.getElementById('couponTotal').value),
    start_time: document.getElementById('couponStartTime').value,
    end_time: document.getElementById('couponEndTime').value
  };
  
  await api('/admin/coupons', { method: 'POST', body: JSON.stringify(data) });
  closeModal('couponModal');
  loadCoupons();
});

document.getElementById('bannerForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('bannerId').value;
  const data = {
    image: document.getElementById('bannerImage').value,
    link: document.getElementById('bannerLink').value,
    sort_order: parseInt(document.getElementById('bannerSortOrder').value)
  };
  
  if (id) {
    await api(`/admin/banners/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  } else {
    await api('/admin/banners', { method: 'POST', body: JSON.stringify(data) });
  }
  closeModal('bannerModal');
  loadBanners();
});

// 工具函数
function formatTime(str) {
  if (!str) return '-';
  const d = new Date(str);
  return `${d.getMonth()+1}/${d.getDate()} ${d.getHours()}:${String(d.getMinutes()).padStart(2,'0')}`;
}

function formatDate(str) {
  if (!str) return '-';
  const d = new Date(str);
  return `${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()}`;
}

function logout() {
  if (confirm('确定退出？')) {
    adminToken = '';
    localStorage.removeItem('adminToken');
    localStorage.removeItem('adminInfo');
    checkAuth();
  }
}

// 初始化
checkAuth();
