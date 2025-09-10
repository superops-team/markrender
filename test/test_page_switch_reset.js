// 页面切换和重置测试脚本
console.log("=== 页面切换和重置测试 ===");

// 模拟页面切换的完整流程
function testPageSwitch(oldItemId, newItemId) {
    console.log(`\n--- 模拟从项目 ${oldItemId} 切换到项目 ${newItemId} ---`);
    
    // 1. 保存当前内容到数据库（在切换前）
    console.log("1. 保存当前内容到数据库");
    saveCurrentContentToDB(oldItemId);
    
    // 2. 重置当前页面
    console.log("2. 重置当前页面");
    resetCurrentPage();
    
    // 3. 加载新内容
    console.log("3. 加载新内容");
    loadNewContentFromDB(newItemId);
}

// 保存当前内容到数据库
function saveCurrentContentToDB(itemId) {
    console.log(`  保存项目 ${itemId} 的内容到数据库`);
    
    if (typeof window.getContent === 'function') {
        try {
            const content = window.getContent();
            if (content) {
                const contentStr = JSON.stringify(content);
                console.log(`  内容大小: ${contentStr.length} 字符`);
                
                // 检查是否为空内容
                const isEmpty = !content.elements || content.elements.length === 0;
                console.log(`  是否为空内容: ${isEmpty}`);
                
                // 模拟保存到数据库
                console.log(`  模拟保存到数据库:`, {
                    item_id: itemId,
                    content_size: contentStr.length,
                    is_empty: isEmpty
                });
                
                // 如果内容为空，应该保存空内容而不是上一个页面的内容
                if (isEmpty) {
                    console.log(`  注意: 保存的是空内容，不应保存上一个页面的内容`);
                }
            } else {
                console.log(`  getContent返回null，保存空内容`);
            }
        } catch (e) {
            console.error(`  保存内容出错:`, e);
        }
    } else {
        console.log(`  getContent函数不存在`);
    }
}

// 重置当前页面
function resetCurrentPage() {
    console.log("  重置当前页面");
    
    // 重置Excalidraw画布
    if (typeof window.reset === 'function') {
        console.log("  调用window.reset()");
        window.reset();
    } else {
        console.log("  reset函数不存在");
    }
    
    // 重置itemId
    if (typeof window.setCurrentItemId === 'function') {
        console.log("  调用window.setCurrentItemId(null)");
        window.setCurrentItemId(null);
    } else {
        console.log("  setCurrentItemId函数不存在");
    }
    
    // 检查重置后的状态
    setTimeout(() => {
        console.log("  重置后检查:");
        if (typeof window.getContent === 'function') {
            const content = window.getContent();
            if (content) {
                const isEmpty = !content.elements || content.elements.length === 0;
                console.log(`  重置后内容是否为空: ${isEmpty}`);
                if (!isEmpty) {
                    console.log("  警告: 重置后内容不为空，可能存在重置不彻底的问题");
                }
            }
        }
    }, 50);
}

// 从数据库加载新内容
function loadNewContentFromDB(itemId) {
    console.log(`  从数据库加载项目 ${itemId} 的内容`);
    
    // 模拟从数据库获取内容
    // 这里应该调用后端接口获取内容
    console.log(`  模拟从数据库获取内容`);
    
    // 设置新itemId
    if (typeof window.setCurrentItemId === 'function') {
        console.log(`  调用window.setCurrentItemId("${itemId}")`);
        window.setCurrentItemId(itemId);
    }
    
    // 加载内容到Excalidraw（如果有的话）
    console.log(`  如果数据库中有内容，则加载到Excalidraw`);
}

// 测试空内容处理
function testEmptyContentHandling() {
    console.log("\n--- 测试空内容处理 ---");
    
    // 1. 创建一个空内容
    console.log("1. 创建空内容");
    const emptyContent = {
        elements: [],
        appState: {},
        itemId: "empty-item-123"
    };
    
    // 2. 设置空内容
    console.log("2. 设置空内容");
    if (typeof window.setValue === 'function') {
        window.setValue(emptyContent);
        console.log("  空内容已设置");
    }
    
    // 3. 获取内容并验证
    console.log("3. 获取内容并验证");
    if (typeof window.getContent === 'function') {
        const content = window.getContent();
        if (content) {
            const isEmpty = !content.elements || content.elements.length === 0;
            console.log(`  当前内容是否为空: ${isEmpty}`);
            console.log(`  元素数量: ${content.elements ? content.elements.length : 0}`);
        }
    }
    
    // 4. 保存空内容
    console.log("4. 保存空内容");
    saveCurrentContentToDB("empty-item-123");
}

// 测试页面复用场景
function testPageReuse() {
    console.log("\n--- 测试页面复用场景 ---");
    
    console.log("场景: 切换到新项目时，页面被复用而不是创建新页面");
    
    // 1. 当前页面有内容
    console.log("1. 当前页面有内容");
    if (typeof window.getContent === 'function') {
        const content = window.getContent();
        if (content) {
            const isEmpty = !content.elements || content.elements.length === 0;
            console.log(`  当前内容是否为空: ${isEmpty}`);
        }
    }
    
    // 2. 切换到新项目
    console.log("2. 切换到新项目");
    console.log("  必须确保:");
    console.log("  a) 保存当前内容到数据库");
    console.log("  b) 重置页面内容为空");
    console.log("  c) 设置新itemId");
    console.log("  d) 从数据库加载新内容（如果有的话）");
    
    // 3. 模拟正确的切换流程
    console.log("3. 模拟正确的切换流程");
    const switchProcess = `
    正确的页面切换流程:
    1. 保存当前内容: saveCurrentContent()
    2. 重置页面: resetPage()
    3. 设置新itemId: setCurrentItemId(newId)
    4. 加载新内容: loadContentFromDB(newId)
    `;
    console.log(switchProcess);
}

// 执行测试
testPageSwitch("item-001", "item-002");
testEmptyContentHandling();
testPageReuse();

console.log("\n=== 测试完成 ===");
console.log("\n建议检查点:");
console.log("1. 重置后页面内容是否真正为空");
console.log("2. 切换项目时是否正确保存了上一个项目的内容");
console.log("3. 是否正确设置了新项目的itemId");
console.log("4. 是否正确加载了新项目的内容");
console.log("5. 页面复用时是否正确重置了状态");