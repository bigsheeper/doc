####一、常用指令
1.从源码生成.ll 
  `clang main.c -emit-llvm -S -c -o main.ll`
2.运行.ll 
  `lli main.ll`
3.编译汇编 
  `llc main.ll`
4.生成dot，得到可视化的DAG
`llc -view-dag-combine1-dags main.ll`
5.将源文件分别编译为LLVM二进制代码
`clang -emit-llvm -c main.c -o main.bc`
6.生成目标文件，通过系统链接器链接多个目标文件，生成可执行文件
`llc -filetype=obj main.bc -o main.o`
`llc -filetype=obj sum.bc -o sum.o`
`clang main.o sum.o -o sum`
7.使用优化器优化 IR/BC 代码，如将Store/Load优化为PHYNode
`opt t.bc -o t.opt.bc -O3`      
`llvm-dis t.opt.bc -o t.opt.ll`


https://segmentfault.com/a/1190000002669213
https://blog.csdn.net/snsn1984/article/details/81041932
https://blog.csdn.net/qq_27885505/article/details/80366525
https://blog.csdn.net/ldzm_edu/article/details/50405182

####二、一些规定
1.One interesting (and very important) aspect of the LLVM IR is that it [requires all basic blocks to be “terminated”](https://llvm.org/docs/LangRef.html#functionstructure) with a [control flow instruction](https://llvm.org/docs/LangRef.html#terminators) such as return or branch. This means that all control flow, *including fall throughs* must be made explicit in the LLVM IR.

2.The body code itself could consist of multiple blocks (e.g. if it contains an if/then/else or a for/in expression).

3.Unlike the C++ code, where the variable v could be either 0 or 1 or any other,but in the LLVM IR it has to be defined only **once**.

####三、建议
1.细分变量，为变量设置标识符，这样可以使得IR代码中不会出现寄存器编号，增加代码的可读性。（IR代码不可以调试）
例如将`builder.CreateStore(builder.CreateLoad(src_i), builder.CreateGEP(dst_ptr, builder.CreateLoad(output_length)));`优化为
`Value *output_idx = builder.CreateLoad(output_length, "output_idx");`
`Value *output_ptr = builder.CreateGEP(dst_ptr, output_idx, "output_ptr");`
`builder.CreateStore(src_i_val, output_ptr);`

####四、代码清单
#####1.IR code
```
int main() {
  LLVMContext &context = TheContext;
  Module *module = new Module("module", context);
  IRBuilder<> builder(context);

  Constant* c = module->getOrInsertFunction("foo",
      /*ret type*/                           builder.getVoidTy(),
      /*args*/                               builder.getInt8PtrTy(),// src_ptr
                                             builder.getInt8Ty(),// target
                                             builder.getInt8PtrTy(),// dst_ptr
                                             builder.getInt8Ty(),// input_length
                                             builder.getInt8PtrTy()// output_length
                                             );

  Function *func = cast<Function>(c);
  func->setCallingConv(CallingConv::C);

  Function::arg_iterator it = func->arg_begin();
  Value* src_ptr = it++;
  Value* target = it++;
  Value* dst_ptr = it++;
  Value* input_length = it++;
  Value* output_length = it++;

  //BasicBlock *entry = BasicBlock::Create(context, "entry", func);
  BasicBlock *initial_i = BasicBlock::Create(context, "InitialI", func);
  BasicBlock *i_less_than_n = BasicBlock::Create(context, "IsIlessThanN", func);
  BasicBlock *op1 = BasicBlock::Create(context, "Operation1", func);
  BasicBlock *op2 = BasicBlock::Create(context, "Operation2", func);
  BasicBlock *increase_i = BasicBlock::Create(context, "IncreaseI", func);
  BasicBlock *ret = BasicBlock::Create(context, "Return", func);

  /// 1.Store/Load method
//  builder.SetInsertPoint(initial_i);
//  AllocaInst *iptr = builder.CreateAlloca(builder.getInt8Ty(), nullptr, "iptr");
//  builder.CreateStore(builder.getInt8(0), iptr);
//  builder.CreateBr(i_less_than_n);
//
//  builder.SetInsertPoint(i_less_than_n);
//  Value* iLessThanN = builder.CreateICmpULT(builder.CreateLoad(iptr), input_length, "cmp");
//  builder.CreateCondBr(iLessThanN, op1, ret);
//
//  builder.SetInsertPoint(op1);
//  Value* src_i = builder.CreateGEP(src_ptr, builder.CreateLoad(iptr), "src[i]");
//  Value* srcGreaterThanTarget = builder.CreateICmpUGT(builder.CreateLoad(src_i), target, "IsSrcIGreaterThanTarget");
//  builder.CreateCondBr(srcGreaterThanTarget, op2, increase_i);
//
//  builder.SetInsertPoint(op2);
//  builder.CreateStore(builder.CreateLoad(src_i), builder.CreateGEP(dst_ptr, builder.CreateLoad(output_length)));
//  Value* new_output_length = builder.CreateAdd(builder.CreateLoad(output_length), builder.getInt8(1));
//  builder.CreateStore(new_output_length, output_length);
//  builder.CreateBr(increase_i);
//
//  builder.SetInsertPoint(increase_i);
//  Value* new_i = builder.CreateAdd(builder.CreateLoad(iptr), builder.getInt8(1), "new_i");
//  builder.CreateStore(new_i, iptr);
//  builder.CreateBr(i_less_than_n);
//
//  builder.SetInsertPoint(ret);
//  builder.CreateRetVoid();

  /// 2.PHINode method
  builder.SetInsertPoint(initial_i);
  Value* i = builder.getInt8(0);
  builder.CreateBr(i_less_than_n);

  builder.SetInsertPoint(i_less_than_n);
  PHINode* phi = builder.CreatePHI(builder.getInt8Ty(), 2, "phi");
  Value* next_v = builder.CreateAdd(phi, builder.getInt8(1), "nextvar");
  phi->addIncoming(i, initial_i);
  phi->addIncoming(next_v, increase_i);
  Value* iLessThanN = builder.CreateICmpULT(phi, input_length, "cmp");
  builder.CreateCondBr(iLessThanN, op1, ret);

  builder.SetInsertPoint(op1);
  Value* src_i = builder.CreateGEP(src_ptr, phi, "src[i]");
  Value* srcGreaterThanTarget = builder.CreateICmpUGT(builder.CreateLoad(src_i), target, "IsSrcIGreaterThanTarget");
  builder.CreateCondBr(srcGreaterThanTarget, op2, increase_i);

  builder.SetInsertPoint(op2);
  builder.CreateStore(builder.CreateLoad(src_i), builder.CreateGEP(dst_ptr, builder.CreateLoad(output_length)));
  Value* new_output_length = builder.CreateAdd(builder.CreateLoad(output_length), builder.getInt8(1));
  builder.CreateStore(new_output_length, output_length);
  builder.CreateBr(increase_i);

  builder.SetInsertPoint(increase_i);
  builder.CreateBr(i_less_than_n);

  builder.SetInsertPoint(ret);
  builder.CreateRetVoid();

  /// Configuring the module
  InitializeAllTargetInfos();
  InitializeAllTargets();
  InitializeAllTargetMCs();
  InitializeAllAsmParsers();
  InitializeAllAsmPrinters();

  auto TargetTriple = sys::getDefaultTargetTriple();
  module->setTargetTriple(TargetTriple);
  std::string Error;
  auto Target = TargetRegistry::lookupTarget(TargetTriple, Error);

  if (!Target) {
    std::cout << "No target\n";
    errs() << Error;
    return 1;
  }

  auto CPU = "generic";
  TargetOptions opt;
  auto RM = Optional<Reloc::Model>();
  auto TheTargetMachine = Target->createTargetMachine(TargetTriple, CPU, "", opt, RM);
  module->setDataLayout(TheTargetMachine->createDataLayout());
  //module->dump();

  /// Emit .o file
  auto Filename = "output.o";
  std::error_code EC;
  raw_fd_ostream dest(Filename, EC, sys::fs::F_None);

  if (EC) {
      std::cout << "Could not open file\n";
      errs() << "Could not open file: " << EC.message();
      return 1;
  }

  legacy::PassManager pass;
  auto FileType = TargetMachine::CGFT_ObjectFile;

  if (TheTargetMachine->addPassesToEmitFile(pass, dest, FileType)) {
      std::cout << "TheTargetMachine can't emit a file of this type\n";
      errs() << "TheTargetMachine can't emit a file of this type";
      return 1;
  }

  pass.run(*module);
  dest.flush();

  outs() << "Wrote " << Filename << "\n";
}
```

#####2.JIT code
```
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/DerivedTypes.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Verifier.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/Host.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Support/TargetRegistry.h"
#include "llvm/Support/TargetSelect.h"
#include "llvm/Target/TargetMachine.h"
#include "llvm/Target/TargetOptions.h"
#include "llvm/Transforms/Scalar.h"
#include "llvm/Transforms/Scalar/GVN.h"
#include "../include/KaleidoscopeJIT.h"
#include <string>
#include <system_error>
#include <iostream>


using namespace llvm;
using namespace llvm::orc;

static LLVMContext context;
static IRBuilder<> builder(context);
static std::unique_ptr<Module> module;
static KaleidoscopeJIT::ModuleHandleT H;
static std::unique_ptr<KaleidoscopeJIT> TheJIT;

typedef void foo_type_t(int32_t *, int32_t, int32_t *, int32_t, int32_t *);

void buildFunction() {
    typedef llvm::FunctionType *pType;

    std::vector<llvm::Type *> func_arg_types;
    func_arg_types.push_back(llvm::Type::getInt32PtrTy(context, 0));
    func_arg_types.push_back(llvm::Type::getInt32Ty(context));
    func_arg_types.push_back(llvm::Type::getInt32PtrTy(context, 0));
    func_arg_types.push_back(llvm::Type::getInt32Ty(context));
    func_arg_types.push_back(llvm::Type::getInt32PtrTy(context, 0));

    pType func_type = llvm::FunctionType::get(llvm::Type::getVoidTy(context),
                                              func_arg_types,
                                              false);

    llvm::Function *func = llvm::Function::Create(func_type, llvm::GlobalValue::ExternalLinkage, "foo", module.get());
    func->setCallingConv(CallingConv::C);

    Function::arg_iterator it = func->arg_begin();
    it->setName("src_ptr");
    Value *src_ptr = it++;
    it->setName("target");
    Value *target = it++;
    it->setName("dst_ptr");
    Value *dst_ptr = it++;
    it->setName("input_length");
    Value *input_length = it++;
    it->setName("output_length");
    Value *output_length = it;

    BasicBlock *initial_i = BasicBlock::Create(context, "InitialI", func);
    BasicBlock *i_less_than_n = BasicBlock::Create(context, "IsIlessThanN", func);
    BasicBlock *op1 = BasicBlock::Create(context, "Operation1", func);
    BasicBlock *op2 = BasicBlock::Create(context, "Operation2", func);
    BasicBlock *increase_i = BasicBlock::Create(context, "IncreaseI", func);
    BasicBlock *ret = BasicBlock::Create(context, "Return", func);

    /// 1.Store/Load method
    builder.SetInsertPoint(initial_i);
    AllocaInst *idx = builder.CreateAlloca(builder.getInt32Ty(), nullptr, "idx");
    builder.CreateStore(builder.getInt32(0), idx);
    builder.CreateBr(i_less_than_n);

    builder.SetInsertPoint(i_less_than_n);
    Value *iLessThanN = builder.CreateICmpSLT(builder.CreateLoad(idx), input_length, "cmp");
    builder.CreateCondBr(iLessThanN, op1, ret);

    builder.SetInsertPoint(op1);
    Value *src_i = builder.CreateGEP(src_ptr, builder.CreateLoad(idx), "src_i_ptr");
    Value *src_i_val = builder.CreateLoad(src_i, "src_i_val");
    Value *srcGreaterThanTarget = builder.CreateICmpSGT(src_i_val, target, "IsSrcIGreaterThanTarget");
    builder.CreateCondBr(srcGreaterThanTarget, op2, increase_i);

    builder.SetInsertPoint(op2);
    Value *output_idx = builder.CreateLoad(output_length, "output_idx");
    Value *output_ptr = builder.CreateGEP(dst_ptr, output_idx, "output_ptr");
    builder.CreateStore(src_i_val, output_ptr);
    output_idx = builder.CreateAdd(output_idx, builder.getInt32(1), "output_idx");
    builder.CreateStore(output_idx, output_length);
    builder.CreateBr(increase_i);

    builder.SetInsertPoint(increase_i);
    Value *next_idx = builder.CreateAdd(builder.CreateLoad(idx), builder.getInt32(1), "next_idx");
    builder.CreateStore(next_idx, idx);
    builder.CreateBr(i_less_than_n);

    builder.SetInsertPoint(ret);
    builder.CreateRetVoid();

    /// 2.PHINode method
//    builder.SetInsertPoint(initial_i);
//    builder.CreateBr(i_less_than_n);
//
//    builder.SetInsertPoint(i_less_than_n);
//    PHINode *idx = builder.CreatePHI(builder.getInt32Ty(), 2, "idx");
//
//    Value *iLessThanN = builder.CreateICmpSLT(idx, input_length, "cmp");
//    builder.CreateCondBr(iLessThanN, op1, ret);
//
//    builder.SetInsertPoint(op1);
//    Value *src_i = builder.CreateGEP(src_ptr, idx, "src_i_ptr");
//    Value *src_val = builder.CreateLoad(src_i,"src_i_val");
//    Value *srcGreaterThanTarget = builder.CreateICmpSGT(src_val, target, "IsSrcIGreaterThanTarget");
//    builder.CreateCondBr(srcGreaterThanTarget, op2, increase_i);
//
//    builder.SetInsertPoint(op2);
//    Value *output_idx = builder.CreateLoad(output_length,"output_idx");
//    Value *output_ptr = builder.CreateGEP(dst_ptr,output_idx,"output_ptr");
//    builder.CreateStore(src_val,output_ptr);
//    output_idx = builder.CreateAdd(output_idx,builder.getInt32(1),"output_idx");
//    builder.CreateStore(output_idx,output_length);
//    builder.CreateBr(increase_i);
//
//    builder.SetInsertPoint(increase_i);
//    Value *next_v = builder.CreateAdd(idx, builder.getInt32(1), "nextvar");
//    idx->addIncoming(builder.getInt32(0), initial_i);
//    idx->addIncoming(next_v, increase_i);
//
//    builder.CreateBr(i_less_than_n);
//
//    builder.SetInsertPoint(ret);
//    builder.CreateRetVoid();
}

foo_type_t *getFunctionPtr() {
    InitializeNativeTarget();
    InitializeNativeTargetAsmPrinter();
    InitializeNativeTargetAsmParser();

    TheJIT = llvm::make_unique<KaleidoscopeJIT>();
    module = llvm::make_unique<Module>("module", context);
    module->setDataLayout(TheJIT->getTargetMachine().createDataLayout());

    buildFunction();

    module->dump();

    H = TheJIT->addModule(std::move(module));
    auto ExprSymbol = TheJIT->findSymbol("foo");
    if (!(ExprSymbol && "Function not found")) {
        std::cout << "Error! Function not found\n";
    }

    auto FP = (foo_type_t *) (intptr_t) cantFail(ExprSymbol.getAddress());

    return FP;
}

int main() {
    int32_t src_ptr[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 0};
    int32_t dst_ptr[10];
    int32_t output_length = 0;

    auto FP = getFunctionPtr();
    FP(src_ptr, 5, dst_ptr, 10, &output_length);

    for (int i = 0; i < output_length; ++i) {
        std::cout << (int) dst_ptr[i] << "\n";
    }

    TheJIT->removeModule(H);
    return 0;
}
```

#####3.optimize the specific pass Code
```
//set(LLVM_LINK_COMPONENTS Passes)
#include "llvm/Passes/PassBuilder.h"

void optimize() {
    llvm::PassBuilder passBuilder;
    llvm::LoopAnalysisManager loopAnalysisManager(true);
    llvm::FunctionAnalysisManager functionAnalysisManager(true);
    llvm::CGSCCAnalysisManager cGSCCAnalysisManager(true);
    llvm::ModuleAnalysisManager moduleAnalysisManager(true);

    passBuilder.registerModuleAnalyses(moduleAnalysisManager);
    passBuilder.registerCGSCCAnalyses(cGSCCAnalysisManager);
    passBuilder.registerFunctionAnalyses(functionAnalysisManager);
    passBuilder.registerLoopAnalyses(loopAnalysisManager);
    passBuilder.crossRegisterProxies(loopAnalysisManager,
                                     functionAnalysisManager,
                                     cGSCCAnalysisManager,
                                     moduleAnalysisManager);

    llvm::ModulePassManager
        modulePassManager = passBuilder.buildPerModuleDefaultPipeline(llvm::PassBuilder::OptimizationLevel::O3);
    modulePassManager.run(*module, moduleAnalysisManager);
}
```

#####4.Full Coding List (including the optimization method)
```
// toy.cpp
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/DerivedTypes.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Verifier.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/Host.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Support/TargetRegistry.h"
#include "llvm/Support/TargetSelect.h"
#include "llvm/Target/TargetMachine.h"
#include "llvm/Target/TargetOptions.h"
#include "llvm/Transforms/Scalar.h"
#include "llvm/Transforms/Scalar/GVN.h"
#include "../include/KaleidoscopeJIT.h"
#include "llvm/Transforms/IPO.h"
#include "llvm/Transforms/IPO/AlwaysInliner.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include <string>
#include <system_error>
#include <iostream>


using namespace llvm;
using namespace llvm::orc;

static LLVMContext context;
static IRBuilder<> builder(context);
static std::unique_ptr<Module> module;
static KaleidoscopeJIT::ModuleHandleT H;
static std::unique_ptr<KaleidoscopeJIT> TheJIT;

typedef void foo_type_t(int32_t *, int32_t, int32_t *, int32_t, int32_t *);

void buildFunction() {
    typedef llvm::FunctionType *pType;

    std::vector<llvm::Type *> func_arg_types;
    func_arg_types.push_back(llvm::Type::getInt32PtrTy(context, 0));
    func_arg_types.push_back(llvm::Type::getInt32Ty(context));
    func_arg_types.push_back(llvm::Type::getInt32PtrTy(context, 0));
    func_arg_types.push_back(llvm::Type::getInt32Ty(context));
    func_arg_types.push_back(llvm::Type::getInt32PtrTy(context, 0));

    pType func_type = llvm::FunctionType::get(llvm::Type::getVoidTy(context),
                                              func_arg_types,
                                              false);

    llvm::Function *func = llvm::Function::Create(func_type, llvm::GlobalValue::ExternalLinkage, "foo", module.get());
    func->setCallingConv(CallingConv::C);

    Function::arg_iterator it = func->arg_begin();
    it->setName("src_ptr");
    Value *src_ptr = it++;
    it->setName("target");
    Value *target = it++;
    it->setName("dst_ptr");
    Value *dst_ptr = it++;
    it->setName("input_length");
    Value *input_length = it++;
    it->setName("output_length");
    Value *output_length = it;

    BasicBlock *initial_i = BasicBlock::Create(context, "InitialI", func);
    BasicBlock *i_less_than_n = BasicBlock::Create(context, "IsIlessThanN", func);
    BasicBlock *op1 = BasicBlock::Create(context, "Operation1", func);
    BasicBlock *op2 = BasicBlock::Create(context, "Operation2", func);
    BasicBlock *increase_i = BasicBlock::Create(context, "IncreaseI", func);
    BasicBlock *ret = BasicBlock::Create(context, "Return", func);

    builder.SetInsertPoint(initial_i);
    AllocaInst *idx = builder.CreateAlloca(builder.getInt32Ty(), nullptr, "idx");
    builder.CreateStore(builder.getInt32(0), idx);
    builder.CreateBr(i_less_than_n);

    builder.SetInsertPoint(i_less_than_n);
    Value *iLessThanN = builder.CreateICmpSLT(builder.CreateLoad(idx), input_length, "cmp");
    builder.CreateCondBr(iLessThanN, op1, ret);

    builder.SetInsertPoint(op1);
    Value *src_i = builder.CreateGEP(src_ptr, builder.CreateLoad(idx), "src_i_ptr");
    Value *src_i_val = builder.CreateLoad(src_i, "src_i_val");
    Value *srcGreaterThanTarget = builder.CreateICmpSGT(src_i_val, target, "IsSrcIGreaterThanTarget");
    builder.CreateCondBr(srcGreaterThanTarget, op2, increase_i);

    builder.SetInsertPoint(op2);
    Value *output_idx = builder.CreateLoad(output_length, "output_idx");
    Value *output_ptr = builder.CreateGEP(dst_ptr, output_idx, "output_ptr");
    builder.CreateStore(src_i_val, output_ptr);
    output_idx = builder.CreateAdd(output_idx, builder.getInt32(1), "output_idx");
    builder.CreateStore(output_idx, output_length);
    builder.CreateBr(increase_i);

    builder.SetInsertPoint(increase_i);
    Value *next_idx = builder.CreateAdd(builder.CreateLoad(idx), builder.getInt32(1), "next_idx");
    builder.CreateStore(next_idx, idx);
    builder.CreateBr(i_less_than_n);

    builder.SetInsertPoint(ret);
    builder.CreateRetVoid();
}

static void AddOptimizationPasses(legacy::PassManager &PM,
                                  TargetMachine *TM) {
    PassManagerBuilder PMB;

    int OptLevel = 3;
    int SizeLevel = 0;
    
    PMB.OptLevel = OptLevel;
    PMB.SizeLevel = SizeLevel;

    PMB.Inliner = createFunctionInliningPass(OptLevel, SizeLevel, false);

    PMB.DisableUnitAtATime = false;
    PMB.DisableUnrollLoops = false;
    PMB.LoopVectorize = true;
    PMB.SLPVectorize = true;

    if (TM) {
        TM->adjustPassManager(PMB);
    }

    PMB.populateModulePassManager(PM);
}

foo_type_t *getFunctionPtr() {
    InitializeNativeTarget();
    InitializeNativeTargetAsmPrinter();
    InitializeNativeTargetAsmParser();

    TheJIT = llvm::make_unique<KaleidoscopeJIT>();
    module = llvm::make_unique<Module>("module", context);
    module->setDataLayout(TheJIT->getTargetMachine().createDataLayout());

    buildFunction();
    module->dump();

    legacy::PassManager PM;
    AddOptimizationPasses(PM, &(TheJIT->getTargetMachine()));
    PM.run(*module);

    std::cout << "\nAfter optimization...\n";
    module->dump();

    H = TheJIT->addModule(std::move(module));

    auto ExprSymbol = TheJIT->findSymbol("foo");
    if (!(ExprSymbol && "Function not found")) {
        std::cout << "Error! Function not found\n";
    }

    auto FP = (foo_type_t *) (intptr_t) cantFail(ExprSymbol.getAddress());

    return FP;
}

int main() {
    int32_t src_ptr[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 0};
    int32_t dst_ptr[10];
    int32_t output_length = 0;

    auto FP = getFunctionPtr();
    FP(src_ptr, 5, dst_ptr, 10, &output_length);

    for (int i = 0; i < output_length; ++i) {
        std::cout << (int) dst_ptr[i] << "\n";
    }

    TheJIT->removeModule(H);
    return 0;
}



//CmakeList
set(LLVM_LINK_COMPONENTS
        #  all
        Analysis
        Core
        ExecutionEngine
        InstCombine
        Object
        RuntimeDyld
        ScalarOpts
        Support
        native
        ipo
        )

add_kaleidoscope_chapter(Kaleidoscope-Ch3
        toy.cpp
        )



//KaleidoscopeJIT.h


//===- KaleidoscopeJIT.h - A simple JIT for Kaleidoscope --------*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// Contains a simple JIT definition for use in the kaleidoscope tutorials.
//
//===----------------------------------------------------------------------===//

#ifndef LLVM_EXECUTIONENGINE_ORC_KALEIDOSCOPEJIT_H
#define LLVM_EXECUTIONENGINE_ORC_KALEIDOSCOPEJIT_H

#include "llvm/ADT/iterator_range.h"
#include "llvm/ADT/STLExtras.h"
#include "llvm/ExecutionEngine/ExecutionEngine.h"
#include "llvm/ExecutionEngine/JITSymbol.h"
#include "llvm/ExecutionEngine/RTDyldMemoryManager.h"
#include "llvm/ExecutionEngine/SectionMemoryManager.h"
#include "llvm/ExecutionEngine/Orc/CompileUtils.h"
#include "llvm/ExecutionEngine/Orc/IRCompileLayer.h"
#include "llvm/ExecutionEngine/Orc/LambdaResolver.h"
#include "llvm/ExecutionEngine/Orc/RTDyldObjectLinkingLayer.h"
#include "llvm/IR/DataLayout.h"
#include "llvm/IR/Mangler.h"
#include "llvm/Support/DynamicLibrary.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Target/TargetMachine.h"
#include <algorithm>
#include <memory>
#include <string>
#include <vector>

namespace llvm {
namespace orc {

class KaleidoscopeJIT {
public:
  using ObjLayerT = RTDyldObjectLinkingLayer;
  using CompileLayerT = IRCompileLayer<ObjLayerT, SimpleCompiler>;
  using ModuleHandleT = CompileLayerT::ModuleHandleT;

  KaleidoscopeJIT()
      : TM(EngineBuilder().selectTarget()), DL(TM->createDataLayout()),
        ObjectLayer([]() { return std::make_shared<SectionMemoryManager>(); }),
        CompileLayer(ObjectLayer, SimpleCompiler(*TM)) {
    llvm::sys::DynamicLibrary::LoadLibraryPermanently(nullptr);
  }

  TargetMachine &getTargetMachine() { return *TM; }

  ModuleHandleT addModule(std::unique_ptr<Module> M) {
    // We need a memory manager to allocate memory and resolve symbols for this
    // new module. Create one that resolves symbols by looking back into the
    // JIT.
    auto Resolver = createLambdaResolver(
        [&](const std::string &Name) {
          if (auto Sym = findMangledSymbol(Name))
            return Sym;
          return JITSymbol(nullptr);
        },
        [](const std::string &S) { return nullptr; });
    auto H = cantFail(CompileLayer.addModule(std::move(M),
                                             std::move(Resolver)));

    ModuleHandles.push_back(H);
    return H;
  }

  void removeModule(ModuleHandleT H) {
    ModuleHandles.erase(find(ModuleHandles, H));
    cantFail(CompileLayer.removeModule(H));
  }

  JITSymbol findSymbol(const std::string Name) {
    return findMangledSymbol(mangle(Name));
  }

private:
  std::string mangle(const std::string &Name) {
    std::string MangledName;
    {
      raw_string_ostream MangledNameStream(MangledName);
      Mangler::getNameWithPrefix(MangledNameStream, Name, DL);
    }
    return MangledName;
  }

  JITSymbol findMangledSymbol(const std::string &Name) {
#ifdef LLVM_ON_WIN32
    // The symbol lookup of ObjectLinkingLayer uses the SymbolRef::SF_Exported
    // flag to decide whether a symbol will be visible or not, when we call
    // IRCompileLayer::findSymbolIn with ExportedSymbolsOnly set to true.
    //
    // But for Windows COFF objects, this flag is currently never set.
    // For a potential solution see: https://reviews.llvm.org/rL258665
    // For now, we allow non-exported symbols on Windows as a workaround.
    const bool ExportedSymbolsOnly = false;
#else
    const bool ExportedSymbolsOnly = true;
#endif

    // Search modules in reverse order: from last added to first added.
    // This is the opposite of the usual search order for dlsym, but makes more
    // sense in a REPL where we want to bind to the newest available definition.
    for (auto H : make_range(ModuleHandles.rbegin(), ModuleHandles.rend()))
      if (auto Sym = CompileLayer.findSymbolIn(H, Name, ExportedSymbolsOnly))
        return Sym;

    // If we can't find the symbol in the JIT, try looking in the host process.
    if (auto SymAddr = RTDyldMemoryManager::getSymbolAddressInProcess(Name))
      return JITSymbol(SymAddr, JITSymbolFlags::Exported);

#ifdef LLVM_ON_WIN32
    // For Windows retry without "_" at beginning, as RTDyldMemoryManager uses
    // GetProcAddress and standard libraries like msvcrt.dll use names
    // with and without "_" (for example "_itoa" but "sin").
    if (Name.length() > 2 && Name[0] == '_')
      if (auto SymAddr =
              RTDyldMemoryManager::getSymbolAddressInProcess(Name.substr(1)))
        return JITSymbol(SymAddr, JITSymbolFlags::Exported);
#endif

    return nullptr;
  }

  std::unique_ptr<TargetMachine> TM;
  const DataLayout DL;
  ObjLayerT ObjectLayer;
  CompileLayerT CompileLayer;
  std::vector<ModuleHandleT> ModuleHandles;
};

} // end namespace orc
} // end namespace llvm

#endif // LLVM_EXECUTIONENGINE_ORC_KALEIDOSCOPEJIT_H
```

#####5.debug
```
Function *get_printf(Module *mod) {
	const char *fun_name = "printf";
	Function *func = mod->getFunction(fun_name);
	if (func == nullptr) {
		FunctionType *func_type = FunctionType::get(
			Type::getInt32Ty(mod->getContext()),
			{Type::getInt8PtrTy(mod->getContext())},
			true);
		func = Function::Create(func_type, GlobalValue::ExternalLinkage, fun_name, mod);
	}
	return func;
}

void Debug(Value *val) {
	auto printf_ptr = get_printf(module.get());
	builder.CreateCall(printf_ptr,
	                   {builder.CreateGlobalStringPtr("[Llvm Debug] value = %lx\n"), val});
}
```

####五、参考
http://llvm.org/docs/
https://llvm.org/docs/tutorial/index.html
http://llvm.org/docs/DebuggingJITedCode.html
http://releases.llvm.org/2.6/docs/tutorial/JITTutorial2.html
http://releases.llvm.org/2.7/docs/UsingLibraries.html
https://stackoverflow.com/questions/31279623/llvm-optimization-using-c-api
**debug**
https://blog.csdn.net/adream307/article/details/83820543
