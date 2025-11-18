(function(){
  // Keys
  const KEY_PRODUCTS = 'farmer_products_v1';
  const KEY_PROFILE = 'farmer_profile_v1';
  const KEY_ORDERS = 'farmer_orders_v1';
  const KEY_PAYMENTS = 'farmer_payments_v1';

  // Sample data fallback
  const sampleProducts = [
    {id:1,name:'Organic Tomatoes (1 kg)',price:40,stock:50,category:'Vegetables',image:'',createdAt:'2025-11-10'},
    {id:2,name:'Fresh Eggs (12 pcs)',price:60,stock:120,category:'Dairy',image:'',createdAt:'2025-11-12'}
  ];
  const sampleOrders = [
    {id:'ORD-1001',buyer:'Ravi Kumar',items:[{name:'Organic Tomatoes',qty:2}],total:80,status:'Delivered',date:'2025-11-15'},
    {id:'ORD-1002',buyer:'Sunita Devi',items:[{name:'Fresh Eggs',qty:1}],total:60,status:'Preparing',date:'2025-11-16'}
  ];
  const samplePayments = [
    {id:'PAY-3001',amount:2500,method:'UPI',date:'2025-11-14',status:'Received'},
    {id:'PAY-3002',amount:5000,method:'Bank Transfer',date:'2025-11-12',status:'Pending'}
  ];
  const defaultProfile = {name:'Laxman Farmer',farmName:'GreenFields Farm',phone:'+91 98765 43210',email:'laxman@example.com',address:'Village XYZ, District, State'};

  // Helpers for localStorage
  function load(key, fallback){ try { const v=localStorage.getItem(key); return v?JSON.parse(v):fallback;}catch(e){return fallback}}
  function save(key, value){ localStorage.setItem(key, JSON.stringify(value)) }

  // Load state
  let products = load(KEY_PRODUCTS, sampleProducts.slice());
  let orders = load(KEY_ORDERS, sampleOrders.slice());
  let payments = load(KEY_PAYMENTS, samplePayments.slice());
  let profile = load(KEY_PROFILE, defaultProfile);

  // DOM refs
  const nav = document.getElementById('nav');
  const pageTitle = document.getElementById('pageTitle');
  const welcomeText = document.getElementById('welcomeText');
  const farmNameSmall = document.getElementById('farmNameSmall');
  const avatar = document.getElementById('avatar');

  const statProducts = document.getElementById('statProducts');
  const statOrders = document.getElementById('statOrders');
  const statEarnings = document.getElementById('statEarnings');
  const statPendingPayments = document.getElementById('statPendingPayments');
  const earningsEl = document.getElementById('earnings');

  const recentOrdersTableBody = document.querySelector('#recentOrdersTable tbody');
  const ordersTableBody = document.querySelector('#ordersTable tbody');
  const paymentsTableBody = document.querySelector('#paymentsTable tbody');

  const productsGrid = document.getElementById('productsGrid');
  const productsCount = document.getElementById('productsCount');
  const productSearch = document.getElementById('productSearch');

  const profileName = document.getElementById('profileName');
  const profileFarm = document.getElementById('profileFarm');
  const profilePhone = document.getElementById('profilePhone');
  const profileEmail = document.getElementById('profileEmail');
  const profileAddress = document.getElementById('profileAddress');

  const productModal = document.getElementById('productModal');
  const addProductBtn = document.getElementById('addProductBtn');
  const newProductBtn = document.getElementById('newProductBtn');
  const quickAdd = document.getElementById('quickAdd');
  const quickOrders = document.getElementById('quickOrders');
  const quickPayments = document.getElementById('quickPayments');

  const productForm = document.getElementById('productForm');
  const pName = document.getElementById('pName');
  const pPrice = document.getElementById('pPrice');
  const pStock = document.getElementById('pStock');
  const pCategory = document.getElementById('pCategory');
  const pImage = document.getElementById('pImage');
  const imgPreview = document.getElementById('imgPreview');
  const closeModal = document.getElementById('closeModal');
  const cancelUpload = document.getElementById('cancelUpload');

  const logoutBtn = document.getElementById('logoutBtn');
  const saveProfileBtn = document.getElementById('saveProfile');
  const clearDataBtn = document.getElementById('clearData');

  // UI update functions
  function renderHeader(){
    pageTitle.textContent = currentTab.charAt(0).toUpperCase()+currentTab.slice(1);
    welcomeText.textContent = `Welcome back, ${profile.name.split(' ')[0]}`;
    farmNameSmall.textContent = profile.farmName;
    avatar.textContent = profile.name.slice(0,1).toUpperCase();
  }

  function calcStats(){
    const totalProducts = products.length;
    const totalOrders = orders.length;
    const earnings = payments.filter(p=>p.status!=='Pending').reduce((s,p)=>s+p.amount,0);
    const pendingPayments = payments.filter(p=>p.status==='Pending').length;
    return {totalProducts,totalOrders,earnings,pendingPayments}
  }

  function renderStats(){
    const s = calcStats();
    statProducts.textContent = s.totalProducts;
    statOrders.textContent = s.totalOrders;
    statEarnings.textContent = s.earnings;
    statPendingPayments.textContent = s.pendingPayments;
    earningsEl.textContent = s.earnings;
  }

  function renderRecentOrders(){
    recentOrdersTableBody.innerHTML = '';
    orders.slice(0,6).forEach(o=>{
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${o.id}</td><td>${o.buyer}</td><td>₹ ${o.total}</td><td>${o.status}</td><td>${o.date}</td>`;
      recentOrdersTableBody.appendChild(tr);
    });
    if(orders.length===0){
      recentOrdersTableBody.innerHTML = '<tr><td colspan="5" class="tiny">No orders yet</td></tr>'
    }
  }

  function renderOrders(){
    ordersTableBody.innerHTML='';
    orders.forEach(o=>{
      const tr = document.createElement('tr');
      const items = o.items.map(i=>`${i.name} x${i.qty}`).join(', ');
      tr.innerHTML = `<td>${o.id}</td><td>${o.buyer}</td><td>${items}</td><td>₹ ${o.total}</td><td>${o.status}</td><td>${o.date}</td>`;
      ordersTableBody.appendChild(tr);
    })
  }

  function renderPayments(){
    paymentsTableBody.innerHTML='';
    payments.forEach(p=>{
      const tr = document.createElement('tr');
      const action = p.status==='Received' ? '' : `<button class="btn" data-pay="${p.id}">Mark received</button>`;
      tr.innerHTML = `<td>${p.id}</td><td>₹ ${p.amount}</td><td>${p.method}</td><td>${p.date}</td><td>${p.status}</td><td>${action}</td>`;
      paymentsTableBody.appendChild(tr);
    })
  }

  function renderProducts(filter=''){
    const q = filter.trim().toLowerCase();
    const filtered = products.filter(p=>p.name.toLowerCase().includes(q));
    productsGrid.innerHTML='';
    filtered.forEach(p=>{
      const div = document.createElement('div');
      div.className = 'product-card';
      div.innerHTML = `
        <div style="height:120px;overflow:hidden;border-radius:8px;">
          ${p.image? `<img src="${p.image}" alt="${p.name}" style="width:100%;height:120px;object-fit:cover">` : `<div class="img-blank">No image</div>`}
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <div style="font-weight:700">${p.name}</div>
          <div class="tiny">₹ ${p.price}</div>
        </div>
        <div class="tiny">${p.category} • ${p.stock} in stock</div>
        <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:8px">
          <button class="btn" data-edit="${p.id}">Edit</button>
          <button class="btn" data-delete="${p.id}" style="color:var(--danger)">Delete</button>
        </div>
      `;
      productsGrid.appendChild(div);
    });
    productsCount.textContent = `${filtered.length} products`;
  }

  function renderProfile(){
    profileName.value = profile.name;
    profileFarm.value = profile.farmName;
    profilePhone.value = profile.phone;
    profileEmail.value = profile.email;
    profileAddress.value = profile.address;
  }

  // Persist helpers
  function persistAll(){
    save(KEY_PRODUCTS, products);
    save(KEY_ORDERS, orders);
    save(KEY_PAYMENTS, payments);
    save(KEY_PROFILE, profile);
  }

  // Event handlers
  function openModal(){
    productModal.style.display='flex';
  }
  function closeModalFn(){
    productModal.style.display='none';
    productForm.reset(); imgPreview.innerHTML='';
  }

  pImage.addEventListener('change', function(e){
    const f = pImage.files && pImage.files[0];
    if(!f) return imgPreview.innerHTML='';
    const reader = new FileReader();
    reader.onload = (ev)=> {
      imgPreview.innerHTML = `<img src="${ev.target.result}" style="height:120px;object-fit:cover;border-radius:8px">`;
      imgPreview.dataset.dataurl = ev.target.result;
    }
    reader.readAsDataURL(f);
  });

  productForm.addEventListener('submit', function(ev){
    ev.preventDefault();
    const newP = {
      id: Date.now(),
      name: pName.value || 'Untitled',
      price: Number(pPrice.value) || 0,
      stock: Number(pStock.value) || 0,
      category: pCategory.value || 'Uncategorized',
      image: imgPreview.dataset.dataurl || '',
      createdAt: new Date().toISOString().split('T')[0]
    };
    products.unshift(newP);
    persistAll(); renderAll();
    closeModalFn();
  });

  closeModal.addEventListener('click', closeModalFn);
  cancelUpload.addEventListener('click', closeModalFn);
  addProductBtn.addEventListener('click', openModal);
  newProductBtn.addEventListener('click', openModal);
  quickAdd.addEventListener('click', openModal);

  // Nav switching
  let currentTab = 'overview';
  nav.addEventListener('click', function(ev){
    const btn = ev.target.closest('button');
    if(!btn) return;
    const tab = btn.dataset.tab;
    if(!tab) return;
    setTab(tab);
  });
  function setTab(tab){
    currentTab = tab;
    document.querySelectorAll('#nav button').forEach(b=>b.classList.toggle('active', b.dataset.tab===tab));
    document.querySelectorAll('.tab-section').forEach(s=>s.style.display='none');
    document.getElementById(tab+'Tab').style.display = 'block';
    renderHeader();
  }

  // Quick actions
  quickOrders.addEventListener('click', ()=>setTab('orders'));
  quickPayments.addEventListener('click', ()=>setTab('payments'));
  document.getElementById('viewAllOrders').addEventListener('click', (e)=>{ e.preventDefault(); setTab('orders') });

  // Products search
  productSearch.addEventListener('input', ()=>renderProducts(productSearch.value));

  // Delegation for product edit/delete & payment mark received
  productsGrid.addEventListener('click', function(ev){
    const del = ev.target.closest('[data-delete]');
    if(del){
      const id = Number(del.dataset.delete);
      if(confirm('Delete this product permanently?')) {
        products = products.filter(p=>p.id!==id);
        persistAll(); renderAll();
      }
      return;
    }
    const edit = ev.target.closest('[data-edit]');
    if(edit){
      const id = Number(edit.dataset.edit);
      const prod = products.find(p=>p.id===id);
      if(!prod) return;
      // present a small inline edit prompt (simple)
      const newName = prompt('Product name', prod.name);
      if(newName===null) return;
      const newPrice = prompt('Price (₹)', prod.price);
      if(newPrice===null) return;
      prod.name = newName;
      prod.price = Number(newPrice) || prod.price;
      persistAll(); renderAll();
    }
  });

  paymentsTableBody.addEventListener('click', function(ev){
    const btn = ev.target.closest('button[data-pay]');
    if(!btn) return;
    const id = btn.dataset.pay;
    const p = payments.find(x=>x.id===id);
    if(!p) return;
    p.status = 'Received';
    persistAll(); renderAll();
  });

  // Orders & payments rendering
  function renderAll(){
    renderHeader(); renderStats(); renderRecentOrders(); renderOrders(); renderPayments(); renderProducts(productSearch.value); renderProfile();
  }

  // Profile save/clear
  saveProfileBtn.addEventListener('click', ()=>{
    profile.name = profileName.value || profile.name;
    profile.farmName = profileFarm.value || profile.farmName;
    profile.phone = profilePhone.value || profile.phone;
    profile.email = profileEmail.value || profile.email;
    profile.address = profileAddress.value || profile.address;
    persistAll(); alert('Profile saved (local demo)');
    renderAll();
  });
  clearDataBtn.addEventListener('click', ()=>{
    if(confirm('Clear all local data (products, orders, payments, profile)?')) {
      localStorage.removeItem(KEY_PRODUCTS);
      localStorage.removeItem(KEY_ORDERS);
      localStorage.removeItem(KEY_PAYMENTS);
      localStorage.removeItem(KEY_PROFILE);
      // reset in-memory
      products = sampleProducts.slice();
      orders = sampleOrders.slice();
      payments = samplePayments.slice();
      profile = defaultProfile;
      renderAll();
      alert('Local demo data cleared');
    }
  });

  // Logout (mock)
  logoutBtn.addEventListener('click', ()=>{
    if(confirm('Log out (demo)?')) {
      // In a real app we'd clear auth cookies / token and redirect to login
      alert('Logged out (demo). You can close the tab or refresh to continue.');
    }
  });

  // View handlers for editing payments/orders via UI can be added similarly

  // Init
  renderAll();

  // Expose small debug API in console
  window._FD = {products,orders,payments,profile,saveAll: persistAll};

})();